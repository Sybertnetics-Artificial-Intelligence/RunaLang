# Runa Compiler Core API

The Runa Compiler Core API provides programmatic access to Runa's compilation pipeline, enabling integration with build systems, IDEs, and custom tooling. This document covers the main compilation interface and core functionality.

## Overview

The Runa compiler is designed as a modular, extensible system that can be used both as a command-line tool and as a library for programmatic compilation. The core API provides access to all stages of the compilation process.

## Core Compilation Interface

### Basic Compilation

```runa
# Example: Basic compilation through API
Process called "compile_runa_code" that takes source as String and target_language as String returns CompilationResult:
    Let compiler be create_compiler with target_language as target_language
    Let result be compile with:
        compiler as compiler
        source as source
        options as default_compilation_options
    Return result
```

### Advanced Compilation with Options

```runa
# Example: Advanced compilation with custom options
Process called "compile_with_options" that takes source as String and config as CompilationConfig returns CompilationResult:
    Let compiler be create_compiler with:
        target_language as config.target_language
        optimization_level as config.optimization_level
        debug_info as config.debug_info
        warnings as config.warnings
    Let result be compile with:
        compiler as compiler
        source as source
        options as config.options
    Return result
```

## Compilation Pipeline

### Stage 1: Lexical Analysis

```runa
# Example: Lexical analysis
Process called "tokenize_source" that takes source as String returns List[Token]:
    Let lexer be create_lexer()
    Let tokens be tokenize with:
        lexer as lexer
        source as source
    Return tokens

# Example: Lexical analysis with error handling
Process called "safe_tokenize" that takes source as String returns Result[List[Token], LexicalError]:
    Try:
        Let tokens be tokenize_source with source as source
        Return Success with value as tokens
    Catch lexical_error as LexicalError:
        Return Error with error as lexical_error
```

### Stage 2: Syntax Analysis

```runa
# Example: Syntax analysis
Process called "parse_tokens" that takes tokens as List[Token] returns AST:
    Let parser be create_parser()
    Let ast be parse with:
        parser as parser
        tokens as tokens
    Return ast

# Example: Syntax analysis with error recovery
Process called "parse_with_recovery" that takes tokens as List[Token] returns ParseResult:
    Let parser be create_parser with error_recovery as true
    Let result be parse_with_recovery with:
        parser as parser
        tokens as tokens
    Return result
```

### Stage 3: Semantic Analysis

```runa
# Example: Semantic analysis
Process called "analyze_semantics" that takes ast as AST returns SemanticResult:
    Let analyzer be create_semantic_analyzer()
    Let result be analyze with:
        analyzer as analyzer
        ast as ast
    Return result

# Example: Type checking
Process called "type_check" that takes ast as AST returns TypeCheckResult:
    Let type_checker be create_type_checker()
    Let result be check_types with:
        type_checker as type_checker
        ast as ast
    Return result
```

### Stage 4: Code Generation

```runa
# Example: Code generation
Process called "generate_code" that takes ast as AST and target_language as String returns GeneratedCode:
    Let generator be create_code_generator with target_language as target_language
    Let code be generate with:
        generator as generator
        ast as ast
    Return code

# Example: Code generation with optimization
Process called "generate_optimized_code" that takes ast as AST and config as GenerationConfig returns GeneratedCode:
    Let generator be create_code_generator with:
        target_language as config.target_language
        optimization_level as config.optimization_level
    Let optimized_ast be optimize_ast with:
        ast as ast
        optimizations as config.optimizations
    Let code be generate with:
        generator as generator
        ast as optimized_ast
    Return code
```

## Compiler Configuration

### Compilation Options

```runa
# Example: Compilation options structure
Type CompilationOptions is Record with:
    target_language as String
    optimization_level as OptimizationLevel
    debug_info as Boolean
    warnings as WarningLevel
    output_format as OutputFormat
    include_paths as List[String]
    define_macros as Dictionary[String, String]
    suppress_warnings as List[String]
    enable_features as List[String]
    disable_features as List[String]

# Example: Creating compilation options
Process called "create_compilation_options" that takes target_language as String returns CompilationOptions:
    Return CompilationOptions with:
        target_language as target_language
        optimization_level as "O1"
        debug_info as true
        warnings as "all"
        output_format as "source"
        include_paths as empty list
        define_macros as empty dictionary
        suppress_warnings as empty list
        enable_features as empty list
        disable_features as empty list
```

### Target Language Configuration

```runa
# Example: Target language specific configuration
Type TargetLanguageConfig is Record with:
    language as String
    version as String
    dialect as String
    features as List[String]
    libraries as List[String]
    compiler_flags as List[String]
    runtime_flags as List[String]

# Example: Python target configuration
Process called "create_python_config" that takes version as String returns TargetLanguageConfig:
    Return TargetLanguageConfig with:
        language as "python"
        version as version
        dialect as "cpython"
        features as list containing "type_hints", "async_await", "f_strings"
        libraries as list containing "typing", "asyncio"
        compiler_flags as list containing "--optimize", "--no-warnings"
        runtime_flags as list containing "-O", "-W", "ignore"
```

## Error Handling and Diagnostics

### Compilation Errors

```runa
# Example: Error handling in compilation
Process called "safe_compile" that takes source as String and target_language as String returns Result[CompilationResult, CompilationError]:
    Try:
        Let result be compile_runa_code with:
            source as source
            target_language as target_language
        Return Success with value as result
    Catch lexical_error as LexicalError:
        Return Error with error as CompilationError with:
            stage as "lexical"
            message as lexical_error.message
            location as lexical_error.location
    Catch parse_error as ParseError:
        Return Error with error as CompilationError with:
            stage as "syntax"
            message as parse_error.message
            location as parse_error.location
    Catch semantic_error as SemanticError:
        Return Error with error as CompilationError with:
            stage as "semantic"
            message as semantic_error.message
            location as semantic_error.location
    Catch generation_error as GenerationError:
        Return Error with error as CompilationError with:
            stage as "code_generation"
            message as generation_error.message
            location as generation_error.location
```

### Diagnostic Reporting

```runa
# Example: Diagnostic collection
Process called "collect_diagnostics" that takes compilation_result as CompilationResult returns List[Diagnostic]:
    Let diagnostics be empty list
    For each error in compilation_result.errors:
        Add Diagnostic with:
            severity as "error"
            message as error.message
            location as error.location
            code as error.code
            source as "runa_compiler"
    For each warning in compilation_result.warnings:
        Add Diagnostic with:
            severity as "warning"
            message as warning.message
            location as warning.location
            code as warning.code
            source as "runa_compiler"
    Return diagnostics
```

## Optimization

### Compiler Optimizations

```runa
# Example: Optimization pipeline
Process called "optimize_ast" that takes ast as AST and optimizations as List[Optimization] returns AST:
    Let optimized_ast be ast
    For each optimization in optimizations:
        Let optimized_ast be apply_optimization with:
            ast as optimized_ast
            optimization as optimization
    Return optimized_ast

# Example: Specific optimizations
Process called "apply_constant_folding" that takes ast as AST returns AST:
    Let folder be create_constant_folder()
    Return fold_constants with:
        folder as folder
        ast as ast

Process called "apply_dead_code_elimination" that takes ast as AST returns AST:
    Let eliminator be create_dead_code_eliminator()
    Return eliminate_dead_code with:
        eliminator as eliminator
        ast as ast

Process called "apply_inlining" that takes ast as AST returns AST:
    Let inliner be create_function_inliner()
    Return inline_functions with:
        inliner as inliner
        ast as ast
```

### Target-Specific Optimizations

```runa
# Example: Python-specific optimizations
Process called "apply_python_optimizations" that takes ast as AST returns AST:
    Let optimized_ast be ast
    Let optimized_ast be apply_constant_folding with ast as optimized_ast
    Let optimized_ast be apply_dead_code_elimination with ast as optimized_ast
    Let optimized_ast be optimize_imports with ast as optimized_ast
    Let optimized_ast be optimize_string_operations with ast as optimized_ast
    Return optimized_ast

# Example: JavaScript-specific optimizations
Process called "apply_javascript_optimizations" that takes ast as AST returns AST:
    Let optimized_ast be ast
    Let optimized_ast be apply_constant_folding with ast as optimized_ast
    Let optimized_ast be apply_dead_code_elimination with ast as optimized_ast
    Let optimized_ast be optimize_arrow_functions with ast as optimized_ast
    Let optimized_ast be optimize_destructuring with ast as optimized_ast
    Return optimized_ast
```

## Incremental Compilation

### Dependency Tracking

```runa
# Example: Dependency analysis
Process called "analyze_dependencies" that takes ast as AST returns DependencyGraph:
    Let analyzer be create_dependency_analyzer()
    Let dependencies be analyze_dependencies with:
        analyzer as analyzer
        ast as ast
    Return dependencies

# Example: Incremental compilation
Process called "incremental_compile" that takes source as String and previous_result as CompilationResult returns CompilationResult:
    Let dependencies be analyze_dependencies with ast as previous_result.ast
    Let changed_modules be detect_changes with:
        dependencies as dependencies
        previous_result as previous_result
    If length of changed_modules is equal to 0:
        Return previous_result
    Otherwise:
        Let affected_modules be get_affected_modules with:
            dependencies as dependencies
            changed_modules as changed_modules
        Return recompile_modules with:
            modules as affected_modules
            source as source
```

## Code Generation

### Source Code Generation

```runa
# Example: Source code generation
Process called "generate_source_code" that takes ast as AST and target_language as String returns String:
    Let generator be create_source_generator with target_language as target_language
    Let source_code be generate_source with:
        generator as generator
        ast as ast
    Return source_code

# Example: Formatted code generation
Process called "generate_formatted_code" that takes ast as AST and target_language as String and formatter as CodeFormatter returns String:
    Let generator be create_source_generator with target_language as target_language
    Let source_code be generate_source with:
        generator as generator
        ast as ast
    Let formatted_code be format_code with:
        formatter as formatter
        code as source_code
        language as target_language
    Return formatted_code
```

### Binary Generation

```runa
# Example: Binary generation
Process called "generate_binary" that takes ast as AST and target_language as String returns Bytes:
    Let generator be create_binary_generator with target_language as target_language
    Let binary be generate_binary with:
        generator as generator
        ast as ast
    Return binary

# Example: Executable generation
Process called "generate_executable" that takes ast as AST and target_language as String and platform as String returns Bytes:
    Let generator be create_executable_generator with:
        target_language as target_language
        platform as platform
    Let executable be generate_executable with:
        generator as generator
        ast as ast
    Return executable
```

## Performance and Monitoring

### Compilation Metrics

```runa
# Example: Compilation metrics collection
Process called "collect_compilation_metrics" that takes compilation_result as CompilationResult returns CompilationMetrics:
    Return CompilationMetrics with:
        lexing_time as compilation_result.lexing_time
        parsing_time as compilation_result.parsing_time
        semantic_analysis_time as compilation_result.semantic_analysis_time
        code_generation_time as compilation_result.code_generation_time
        total_time as compilation_result.total_time
        memory_usage as compilation_result.memory_usage
        source_lines as compilation_result.source_lines
        generated_lines as compilation_result.generated_lines
        optimization_count as compilation_result.optimization_count
```

### Performance Profiling

```runa
# Example: Compilation profiling
Process called "profile_compilation" that takes source as String and target_language as String returns CompilationProfile:
    Let profiler be create_compilation_profiler()
    Let profile be profile_compilation with:
        profiler as profiler
        source as source
        target_language as target_language
    Return profile
```

## Testing and Validation

### Compilation Testing

```runa
# Example: Compilation test
Test "basic_compilation":
    Let source be "Let x be 42"
    Let result be compile_runa_code with:
        source as source
        target_language as "python"
    Assert result.success is true
    Assert result.generated_code is not empty
    Assert result.errors is empty

# Example: Error testing
Test "compilation_error_handling":
    Let invalid_source be "Let x be"  # Missing value
    Let result be compile_runa_code with:
        source as invalid_source
        target_language as "python"
    Assert result.success is false
    Assert length of result.errors is greater than 0
```

### Round-Trip Testing

```runa
# Example: Round-trip compilation test
Test "round_trip_compilation":
    Let original_source be "Let x be 42\nLet y be x multiplied by 2"
    Let result1 be compile_runa_code with:
        source as original_source
        target_language as "python"
    Let result2 be compile_runa_code with:
        source as original_source
        target_language as "javascript"
    Assert result1.success is true
    Assert result2.success is true
    Assert result1.generated_code is not equal to result2.generated_code
```

## API Reference

### Core Classes

- `Compiler` - Main compiler interface
- `Lexer` - Lexical analysis
- `Parser` - Syntax analysis
- `SemanticAnalyzer` - Semantic analysis
- `TypeChecker` - Type checking
- `CodeGenerator` - Code generation
- `Optimizer` - Code optimization

### Key Methods

- `compile(source, target_language, options)` - Main compilation method
- `tokenize(source)` - Lexical analysis
- `parse(tokens)` - Syntax analysis
- `analyze(ast)` - Semantic analysis
- `generate(ast, target_language)` - Code generation
- `optimize(ast, optimizations)` - Code optimization
- `validate(ast)` - AST validation

### Configuration Types

- `CompilationOptions` - Compilation configuration
- `TargetLanguageConfig` - Target language configuration
- `OptimizationLevel` - Optimization level enumeration
- `WarningLevel` - Warning level enumeration
- `OutputFormat` - Output format enumeration

### Result Types

- `CompilationResult` - Compilation result
- `ParseResult` - Parsing result
- `SemanticResult` - Semantic analysis result
- `TypeCheckResult` - Type checking result
- `GeneratedCode` - Generated code result
- `CompilationError` - Compilation error
- `CompilationMetrics` - Compilation performance metrics

This compiler API provides comprehensive access to Runa's compilation pipeline, enabling integration with build systems, IDEs, and custom development tools while maintaining the language's natural syntax philosophy. 