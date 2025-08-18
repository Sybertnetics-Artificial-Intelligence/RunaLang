# Macros System Core Module

## Overview

The Macros System Core module provides the foundational infrastructure for macro processing in Runa. It handles macro definition, registration, expansion pipeline management, caching, and debugging capabilities. This module serves as the central registry and orchestrator for all macro operations.

## Key Features

- **Macro Registry**: Centralized registry for macro definitions and metadata
- **Expansion Pipeline**: Efficient macro expansion with caching and performance optimization
- **Hygiene System**: Automatic variable scoping and name collision prevention
- **Cross-Module Support**: Macros can be shared and used across different modules
- **Versioning**: Comprehensive macro versioning and compatibility management
- **Debugging Tools**: Rich introspection and debugging capabilities for macro development
- **Production Ready**: Enterprise-grade performance with caching and error handling

## Core Types

### MacroConfig
```runa
Type called "MacroConfig":
    enabled as Boolean defaults to true
    expansion_limit as Integer defaults to 1000
    enable_caching as Boolean defaults to true
    enable_debugging as Boolean defaults to false
    enable_introspection as Boolean defaults to true
    enable_cross_module as Boolean defaults to true
    enable_versioning as Boolean defaults to true
    cache_size as Integer defaults to 1048576
    metadata as Dictionary[String, Any] defaults to empty dictionary
```

Configuration for macro system behavior including performance limits, feature toggles, and debugging options.

### MacroDefinition
```runa
Type called "MacroDefinition":
    name as String
    version as String
    macro_type as String
    pattern as MacroPattern
    template as MacroTemplate
    hygiene_rules as List[HygieneRule]
    compilation_flags as Dictionary[String, Any]
    metadata as Dictionary[String, Any]
```

Complete definition of a macro including its pattern matching rules, code generation template, and hygiene configuration.

### MacroContext
```runa
Type called "MacroContext":
    config as MacroConfig
    registry as MacroRegistry
    expansion_stack as List[ExpansionFrame]
    cache as MacroCache
    debug_info as Dictionary[String, Any]
    performance_metrics as Dictionary[String, Float]
    metadata as Dictionary[String, Any]
```

The main context object that manages all macro operations and maintains state during expansion.

## Main Functions

### Context Management

#### create_macro_context
```runa
Process called "create_macro_context" that takes config as Optional[MacroConfig] returns MacroContext:
    Note: Create a new macro context with specified or default configuration
```

**Parameters:**
- `config` (Optional[MacroConfig]): Configuration for the macro system, uses defaults if None

**Returns:** MacroContext ready for macro operations

**Example:**
```runa
Import "advanced/macros/system" as Macros

Note: Create context with default configuration
Let default_context be Macros.create_macro_context with config as None

Note: Create context with custom configuration
Let custom_config be Macros.MacroConfig with:
    enabled as true
    expansion_limit as 500
    enable_caching as true
    enable_debugging as true
    enable_introspection as true
    cache_size as 2097152  Note: 2MB cache

Let custom_context be Macros.create_macro_context with config as custom_config

Display "Macro context created with cache size: " plus custom_context.config.cache_size
```

### Macro Registration

#### register_macro
```runa
Process called "register_macro" that takes context as MacroContext and macro_def as MacroDefinition returns Boolean:
    Note: Register a macro definition in the context registry
```

**Parameters:**
- `context` (MacroContext): The macro context to register in
- `macro_def` (MacroDefinition): Complete macro definition to register

**Returns:** Boolean indicating success or failure

**Example:**
```runa
Note: Create a debug printing macro
Let debug_macro be Macros.MacroDefinition with:
    name as "debug_print"
    version as "1.0.0"
    macro_type as "function_like"
    pattern as Macros.MacroPattern with:
        syntax as "debug_print!($expr)"
        tokens as list containing
        variables as list containing "expr"
        constraints as list containing
        metadata as dictionary containing
    template as Macros.MacroTemplate with:
        template_code as "Display \"DEBUG: \" plus $expr"
        ast_template as create_debug_ast_template()
        variable_mappings as dictionary containing "expr" as "expression"
        conditional_sections as list containing
        metadata as dictionary containing
    hygiene_rules as list containing
    compilation_flags as dictionary containing "optimize" as true
    metadata as dictionary containing "author" as "Runa Team"

Let registration_success be Macros.register_macro with 
    context as macro_context 
    and macro_def as debug_macro

If registration_success:
    Display "Debug macro registered successfully"
Otherwise:
    Display "Failed to register debug macro"
```

### Macro Expansion

#### expand_macro
```runa
Process called "expand_macro" that takes context as MacroContext and macro_name as String and input_tokens as List[Token] returns ExpansionResult:
    Note: Expand a registered macro with given input tokens
```

**Parameters:**
- `context` (MacroContext): The macro context containing registered macros
- `macro_name` (String): Name of the macro to expand
- `input_tokens` (List[Token]): Input tokens to process with the macro

**Returns:** ExpansionResult containing success/failure and generated code

**Example:**
```runa
Note: Create input tokens for macro expansion
Let input_tokens be list containing:
    Macros.Token with:
        type as "identifier"
        value as "user_count"
        position as Macros.Position with line as 1 and column as 1 and offset as 0 and metadata as dictionary containing
        metadata as dictionary containing

Note: Expand the debug macro
Let expansion_result be Macros.expand_macro with 
    context as macro_context 
    and macro_name as "debug_print" 
    and input_tokens as input_tokens

Match expansion_result:
    Case ExpansionSuccess with tokens and ast and performance_metrics:
        Display "Macro expansion successful!"
        Display "Generated " plus length of tokens plus " tokens"
        Display "Expansion time: " plus performance_metrics["expansion_time"] plus "ms"
        
        Note: Use the expanded tokens
        For each token in tokens:
            Display "Token: " plus token.type plus " = " plus token.value
            
    Case ExpansionError with error and details:
        Display "Macro expansion failed: " plus error
        If "line" in details:
            Display "Error at line " plus details["line"]
            
    Case ExpansionWarning with warning and tokens and ast:
        Display "Macro expansion succeeded with warning: " plus warning
        Display "Generated " plus length of tokens plus " tokens"
```

### Registry Management

#### get_macro
```runa
Process called "get_macro" that takes context as MacroContext and name as String returns Optional[MacroDefinition]:
    Note: Retrieve a macro definition by name
```

**Example:**
```runa
Let macro_def be Macros.get_macro with context as macro_context and name as "debug_print"

If macro_def is not None:
    Display "Found macro: " plus macro_def.name plus " version " plus macro_def.version
    Display "Macro type: " plus macro_def.macro_type
Otherwise:
    Display "Macro not found"
```

#### list_macros
```runa
Process called "list_macros" that takes context as MacroContext returns List[String]:
    Note: Get list of all registered macro names
```

**Example:**
```runa
Let macro_names be Macros.list_macros with context as macro_context

Display "Registered macros:"
For each name in macro_names:
    Let macro_def be Macros.get_macro with context as macro_context and name as name
    Display "  " plus name plus " (v" plus macro_def.version plus ")"
```

#### unregister_macro
```runa
Process called "unregister_macro" that takes context as MacroContext and name as String returns Boolean:
    Note: Remove a macro from the registry
```

**Example:**
```runa
Let removal_success be Macros.unregister_macro with 
    context as macro_context 
    and name as "debug_print"

If removal_success:
    Display "Macro removed successfully"
Otherwise:
    Display "Failed to remove macro (not found)"
```

## Advanced Features

### Macro Validation

The system automatically validates macro definitions during registration:

```runa
Note: Example of validation that occurs automatically
Process called "validate_macro_definition" that takes macro_def as MacroDefinition returns Boolean:
    Note: Validates macro name, pattern, template, and hygiene rules
```

Validation checks include:
- Non-empty macro name
- Valid pattern syntax
- Complete template definition
- Proper hygiene rule configuration
- Constraint consistency

### Performance Monitoring

The macro system provides detailed performance metrics:

```runa
Note: Access performance metrics
Let context be Macros.create_macro_context with config as None

Note: After macro operations, check performance
Display "Performance Metrics:"
Display "  Registration time: " plus context.performance_metrics["registration_time"] plus "ms"
Display "  Expansion time: " plus context.performance_metrics["expansion_time"] plus "ms"
Display "  Cache hit rate: " plus calculate_cache_hit_rate(context.cache)
```

### Caching System

Automatic caching improves performance for repeated macro expansions:

```runa
Note: Caching is automatic but can be configured
Let caching_config be Macros.MacroConfig with:
    enable_caching as true
    cache_size as 4194304  Note: 4MB cache

Let cached_context be Macros.create_macro_context with config as caching_config

Note: First expansion - will be cached
Let result1 be Macros.expand_macro with 
    context as cached_context 
    and macro_name as "debug_print" 
    and input_tokens as input_tokens

Note: Second expansion - uses cache
Let result2 be Macros.expand_macro with 
    context as cached_context 
    and macro_name as "debug_print" 
    and input_tokens as input_tokens

Note: Second expansion should be faster due to caching
```

### Cross-Module Macro Support

Macros can be shared across modules:

```runa
Note: Register a macro for cross-module use
Let utility_macro be create_utility_macro()
Let registration_success be Macros.register_macro with 
    context as shared_context 
    and macro_def as utility_macro

Note: The macro is now available in other modules that use this context
```

### Versioning and Compatibility

The system supports macro versioning:

```runa
Note: Register multiple versions of the same macro
Let debug_v1 be create_debug_macro_v1()
Let debug_v2 be create_debug_macro_v2()

Macros.register_macro with context as versioned_context and macro_def as debug_v1
Macros.register_macro with context as versioned_context and macro_def as debug_v2

Note: List all versions
Let versions be versioned_context.registry.version_registry["debug_print"]
Display "Available versions: " plus join_strings(versions, ", ")
```

## Error Handling

The macro system provides comprehensive error handling:

```runa
Note: Handle various types of errors
Let expansion_result be Macros.expand_macro with 
    context as macro_context 
    and macro_name as "nonexistent_macro" 
    and input_tokens as input_tokens

Match expansion_result:
    Case ExpansionError with error and details:
        Match error:
            Case "Macro system is disabled":
                Display "Enable macro system in configuration"
            Case "Expansion limit exceeded":
                Display "Increase expansion_limit in configuration"
            Case error if error contains "Macro not found":
                Display "Register the macro first: " plus extract_macro_name(error)
            Case "Failed to match macro pattern":
                Display "Check input tokens match macro pattern"
            Case default:
                Display "Unexpected error: " plus error
```

## Best Practices

### Configuration
```runa
Note: Production configuration
Let production_config be Macros.MacroConfig with:
    enabled as true
    expansion_limit as 10000        Note: Higher limit for production
    enable_caching as true          Note: Essential for performance
    enable_debugging as false       Note: Disable in production
    enable_introspection as false   Note: Disable for security
    enable_cross_module as true     Note: Enable for modularity
    enable_versioning as true       Note: Enable for compatibility
    cache_size as 16777216         Note: 16MB cache for production

Note: Development configuration
Let development_config be Macros.MacroConfig with:
    enabled as true
    expansion_limit as 1000
    enable_caching as true
    enable_debugging as true        Note: Enable for development
    enable_introspection as true    Note: Enable for debugging
    enable_cross_module as true
    enable_versioning as true
    cache_size as 4194304          Note: 4MB cache for development
```

### Macro Design Patterns
```runa
Note: Function-like macro pattern
Let function_like_pattern be Macros.MacroPattern with:
    syntax as "macro_name!($arg1, $arg2)"
    variables as list containing "arg1", "arg2"
    constraints as list containing

Note: Attribute-like macro pattern  
Let attribute_pattern be Macros.MacroPattern with:
    syntax as "#[macro_name($arg)]"
    variables as list containing "arg"
    constraints as list containing

Note: Block macro pattern
Let block_pattern be Macros.MacroPattern with:
    syntax as "macro_name! { $body }"
    variables as list containing "body"
    constraints as list containing
```

### Error Prevention
```runa
Note: Always validate inputs
Process called "safe_macro_expansion" that takes context as MacroContext and name as String and tokens as List[Token] returns Boolean:
    If not context.config.enabled:
        Display "Macro system is disabled"
        Return false
    
    Let macro_def be Macros.get_macro with context as context and name as name
    If macro_def is None:
        Display "Macro not found: " plus name
        Return false
    
    Let result be Macros.expand_macro with context as context and macro_name as name and input_tokens as tokens
    Return result is ExpansionSuccess
```

This system module provides the solid foundation needed for all macro operations in Runa, with enterprise-grade performance, comprehensive error handling, and extensive debugging capabilities.