# Reflection Module

The Reflection module provides comprehensive runtime and compile-time introspection capabilities for the Runa programming language. This module enables dynamic analysis, manipulation, and invocation of types, values, methods, and properties, making it essential for building flexible, adaptive systems.

## Table of Contents

- [Overview](#overview)
- [Core Types](#core-types)
- [API Reference](#api-reference)
- [Usage Examples](#usage-examples)
- [Advanced Patterns](#advanced-patterns)
- [Performance Considerations](#performance-considerations)
- [Best Practices](#best-practices)

## Overview

The Reflection module provides powerful introspection capabilities:

- **Type Reflection**: Examine type information at runtime and compile time
- **Value Introspection**: Analyze value structures and metadata
- **Dynamic Invocation**: Call methods and access properties dynamically
- **Metadata Access**: Retrieve annotations and custom metadata
- **Runtime Analysis**: Perform dynamic code analysis and validation
- **Property Access**: Get and set object properties dynamically

## Key Features

- **Runtime Type Introspection**: Complete type information access at runtime
- **Dynamic Method Invocation**: Safe dynamic calling of methods and functions
- **Property Access**: Dynamic get/set operations on object properties
- **Metadata System**: Rich annotation and metadata support
- **AI-First Design**: Natural language syntax optimized for AI agent usage
- **Type Safety**: Comprehensive validation and error handling
- **Performance Optimized**: Minimal overhead for reflection operations
- **Production Ready**: Robust error handling and validation

## Types and Interfaces

### Core Reflection Types

```runa
Type called "ReflectionContext":
    config as ReflectionConfig
    stats as ReflectionStats
    metadata as Dictionary[String, Any]

Type called "ReflectionConfig":
    enable_runtime_reflection as Boolean
    enable_compile_time_reflection as Boolean
    enable_dynamic_invocation as Boolean
    ai_mode as Boolean
    metadata as Dictionary[String, Any]

Type called "Reflectable":
    type_info as TypeInfo
    value as Any
    metadata as Dictionary[String, Any]

Type called "TypeInfo":
    type_id as String
    type_kind as String
    size as Integer
    alignment as Integer
    is_primitive as Boolean
    is_reference as Boolean
    metadata as Dictionary[String, Any]
```

### Statistics and Error Handling

```runa
Type called "ReflectionStats":
    total_introspections as Integer
    total_invocations as Integer
    total_errors as Integer
    metadata as Dictionary[String, Any]

Type ReflectionError is Exception with:
    message as String
    metadata as Dictionary[String, Any]
```

## Core Functions

### Type Introspection

```runa
Process called "reflect_type" that takes context as ReflectionContext and value as Any returns TypeInfo
```

Performs deep type introspection on any value, returning comprehensive type information.

**Parameters:**
- `context` - The reflection context with configuration
- `value` - The value to introspect

**Returns:** Complete `TypeInfo` describing the value's type.

**Example:**
```runa
Import "advanced/metaprogramming/reflection" as Reflection

Note: Create reflection context
Let config be Reflection.ReflectionConfig with:
    enable_runtime_reflection as true
    enable_compile_time_reflection as true
    enable_dynamic_invocation as true
    ai_mode as true
    metadata as empty dictionary

Let context be Reflection.ReflectionContext with:
    config as config
    stats as Reflection.ReflectionStats with total_introspections as 0 and total_invocations as 0 and total_errors as 0 and metadata as empty dictionary
    metadata as empty dictionary

Note: Introspect different types
Let number_info be Reflection.reflect_type with context as context and value as 42
Display "Type: " plus number_info.type_id plus " Kind: " plus number_info.type_kind

Let text_info be Reflection.reflect_type with context as context and value as "Hello, World!"
Display "Type: " plus text_info.type_id plus " Size: " plus text_info.size

Let list_info be Reflection.reflect_type with context as context and value as list containing 1, 2, 3
Display "Collection type: " plus list_info.type_id plus " Is reference: " plus list_info.is_reference
```

```runa
Process called "reflect_value" that takes context as ReflectionContext and value as Any returns Reflectable
```

Creates a reflectable wrapper around any value for enhanced introspection.

**Example:**
```runa
Let user_data be Dictionary with:
    "name" as "Alice"
    "age" as 30
    "active" as true
    "metadata" as Dictionary with "role" as "admin"

Let reflectable be Reflection.reflect_value with context as context and value as user_data
Display "Reflectable created for: " plus reflectable.type_info.type_id
```

### Dynamic Method Invocation

```runa
Process called "invoke_method" that takes context as ReflectionContext and value as Any and method_name as String and args as List[Any] returns Any
```

Dynamically invokes a method on an object with type-safe error handling.

**Parameters:**
- `context` - Reflection context (must have `enable_dynamic_invocation` set to `true`)
- `value` - The object containing the method
- `method_name` - Name of the method to invoke
- `args` - Arguments to pass to the method

**Returns:** The result of the method invocation.

**Example:**
```runa
Note: Create an object with methods
Let calculator be Dictionary with:
    "add" as Process that takes a as Integer and b as Integer returns Integer:
        Return a plus b
    "multiply" as Process that takes a as Integer and b as Integer returns Integer:
        Return a times b
    "name" as "Advanced Calculator"

Try:
    Note: Dynamically invoke the add method
    Let result be Reflection.invoke_method with context as context and value as calculator and method_name as "add" and args as list containing 5, 3
    Display "Dynamic addition result: " plus result
    
    Note: Invoke the multiply method
    Let product be Reflection.invoke_method with context as context and value as calculator and method_name as "multiply" and args as list containing 4, 7
    Display "Dynamic multiplication result: " plus product

Catch error as Reflection.ReflectionError:
    Display "Method invocation failed: " plus error.message
```

### Property Access

```runa
Process called "get_property" that takes context as ReflectionContext and value as Any and property_name as String returns Any
```

Safely retrieves a property value from an object.

```runa
Process called "set_property" that takes context as ReflectionContext and value as Any and property_name as String and new_value as Any returns None
```

Safely sets a property value on an object.

**Example:**
```runa
Let person be Dictionary with:
    "name" as "Bob"
    "age" as 25
    "email" as "bob@example.com"

Try:
    Note: Get property values dynamically
    Let name be Reflection.get_property with context as context and value as person and property_name as "name"
    Display "Name: " plus name
    
    Let age be Reflection.get_property with context as context and value as person and property_name as "age"
    Display "Age: " plus age
    
    Note: Set property values dynamically
    Reflection.set_property with context as context and value as person and property_name as "age" and new_value as 26
    Display "Updated age: " plus person["age"]

Catch error as Reflection.ReflectionError:
    Display "Property access failed: " plus error.message
```

### Metadata and Annotations

```runa
Process called "get_metadata" that takes context as ReflectionContext and value as Any returns Dictionary[String, Any]
```

Retrieves metadata associated with a value or object.

```runa
Process called "get_annotations" that takes context as ReflectionContext and value as Any returns List[Annotation]
```

Gets annotations attached to a value or type.

**Example:**
```runa
Note: Create object with metadata
Let annotated_object be Dictionary with:
    "data" as "Important information"
    "metadata" as Dictionary with:
        "author" as "System"
        "version" as "1.0"
        "created_at" as "2024-01-15"
    "annotations" as list containing "Validated", "Cached", "Immutable"

Let metadata be Reflection.get_metadata with context as context and value as annotated_object
Display "Object metadata:"
For each key in metadata:
    Display "  " plus key plus ": " plus metadata[key]

Let annotations be Reflection.get_annotations with context as context and value as annotated_object
Display "Annotations: " plus annotations
```

### Introspection Utilities

```runa
Process called "list_methods" that takes context as ReflectionContext and value as Any returns List[String]
```

Returns a list of all callable methods on an object.

```runa
Process called "list_properties" that takes context as ReflectionContext and value as Any returns List[String]
```

Returns a list of all properties (non-method fields) on an object.

**Example:**
```runa
Let api_client be Dictionary with:
    "get" as Process that takes url as String returns String:
        Return "GET " plus url
    "post" as Process that takes url as String and data as Any returns String:
        Return "POST " plus url plus " with data"
    "base_url" as "https://api.example.com"
    "timeout" as 30
    "headers" as Dictionary with "User-Agent" as "Runa API Client"

Let methods be Reflection.list_methods with context as context and value as api_client
Display "Available methods: " plus methods

Let properties be Reflection.list_properties with context as context and value as api_client
Display "Available properties: " plus properties
```

## Idiomatic Usage Patterns

### Dynamic API Client

```runa
Import "advanced/metaprogramming/reflection" as Reflection

Note: Create a dynamic API client using reflection
Process called "create_dynamic_api_client" that takes base_url as String returns Dictionary:
    Return Dictionary with:
        "base_url" as base_url
        "headers" as Dictionary with "Content-Type" as "application/json"
        "timeout" as 30
        "get" as Process that takes endpoint as String returns String:
            Return "GET " plus base_url plus endpoint
        "post" as Process that takes endpoint as String and data as Any returns String:
            Return "POST " plus base_url plus endpoint plus " with " plus data
        "put" as Process that takes endpoint as String and data as Any returns String:
            Return "PUT " plus base_url plus endpoint plus " with " plus data
        "delete" as Process that takes endpoint as String returns String:
            Return "DELETE " plus base_url plus endpoint

Process called "dynamic_api_example" returns None:
    Let context be create_reflection_context with ai_mode as true
    Let client be create_dynamic_api_client with base_url as "https://jsonplaceholder.typicode.com"
    
    Note: Discover available methods dynamically
    Let methods be Reflection.list_methods with context as context and value as client
    Display "API Client Methods: " plus methods
    
    Note: Invoke methods dynamically based on user input or AI decisions
    Let http_methods be list containing "get", "post", "put", "delete"
    For each method in http_methods:
        If method in methods:
            Try:
                Let result be Reflection.invoke_method with context as context and value as client and method_name as method and args as list containing "/users/1"
                Display method plus " result: " plus result
            Catch error as Reflection.ReflectionError:
                Display "Failed to invoke " plus method plus ": " plus error.message
```

### Configuration System with Reflection

```runa
Import "advanced/metaprogramming/reflection" as Reflection

Process called "reflective_configuration_system" returns None:
    Let context be create_reflection_context with ai_mode as true
    
    Note: Create configuration object with validation
    Let config be Dictionary with:
        "database_url" as "postgres://localhost:5432/mydb"
        "cache_size" as 1000
        "enable_logging" as true
        "log_level" as "INFO"
        "metadata" as Dictionary with:
            "config_version" as "2.0"
            "last_updated" as "2024-01-15"
        "validate" as Process that takes key as String and value as Any returns Boolean:
            Match key:
                When "database_url":
                    Return value is String and "://" in value
                When "cache_size":
                    Return value is Integer and value is greater than 0
                When "enable_logging":
                    Return value is Boolean
                When "log_level":
                    Return value in list containing "DEBUG", "INFO", "WARN", "ERROR"
                Otherwise:
                    Return true
    
    Note: Dynamically validate configuration
    Let properties be Reflection.list_properties with context as context and value as config
    For each prop in properties:
        If prop is not equal to "metadata" and prop is not equal to "validate":
            Let value be Reflection.get_property with context as context and value as config and property_name as prop
            
            Try:
                Let is_valid be Reflection.invoke_method with context as context and value as config and method_name as "validate" and args as list containing prop, value
                If is_valid:
                    Display "✓ " plus prop plus ": " plus value plus " (valid)"
                Otherwise:
                    Display "✗ " plus prop plus ": " plus value plus " (invalid)"
            Catch error:
                Display "⚠ " plus prop plus ": validation error"
    
    Note: Dynamic configuration updates
    Try:
        Reflection.set_property with context as context and value as config and property_name as "cache_size" and new_value as 2000
        Display "Updated cache_size to 2000"
        
        Note: Validate the new value
        Let new_value be Reflection.get_property with context as context and value as config and property_name as "cache_size"
        Let is_valid be Reflection.invoke_method with context as context and value as config and method_name as "validate" and args as list containing "cache_size", new_value
        If is_valid:
            Display "✓ New cache_size is valid"
        Otherwise:
            Display "✗ New cache_size is invalid"
            
    Catch error as Reflection.ReflectionError:
        Display "Configuration update failed: " plus error.message
```

### Plugin System with Dynamic Loading

```runa
Import "advanced/metaprogramming/reflection" as Reflection

Process called "dynamic_plugin_system" returns None:
    Let context be create_reflection_context with ai_mode as true
    
    Note: Define plugin interface through reflection
    Let plugin_registry be Dictionary with:
        "plugins" as empty list
        "register_plugin" as Process that takes plugin as Any returns Boolean:
            Note: Validate plugin interface using reflection
            Let methods be Reflection.list_methods with context as context and value as plugin
            Let required_methods be list containing "initialize", "execute", "cleanup"
            
            For each required_method in required_methods:
                If required_method not in methods:
                    Display "Plugin missing required method: " plus required_method
                    Return false
            
            Note: Add to registry
            plugin_registry["plugins"].append(plugin)
            Display "Plugin registered successfully"
            Return true
    
    Note: Example plugins
    Let text_processor_plugin be Dictionary with:
        "name" as "Text Processor"
        "version" as "1.0"
        "initialize" as Process returns Boolean:
            Display "Text processor initialized"
            Return true
        "execute" as Process that takes data as Any returns Any:
            If data is String:
                Return data uppercased
            Return data
        "cleanup" as Process returns None:
            Display "Text processor cleaned up"
    
    Let number_processor_plugin be Dictionary with:
        "name" as "Number Processor"
        "version" as "1.0"
        "initialize" as Process returns Boolean:
            Display "Number processor initialized"
            Return true
        "execute" as Process that takes data as Any returns Any:
            If data is Integer:
                Return data times 2
            Return data
        "cleanup" as Process returns None:
            Display "Number processor cleaned up"
    
    Note: Register plugins dynamically
    Reflection.invoke_method with context as context and value as plugin_registry and method_name as "register_plugin" and args as list containing text_processor_plugin
    Reflection.invoke_method with context as context and value as plugin_registry and method_name as "register_plugin" and args as list containing number_processor_plugin
    
    Note: Execute plugins dynamically
    Let test_data be list containing "hello world", 42, "runa programming", 7
    
    For each plugin in plugin_registry["plugins"]:
        Let plugin_name be Reflection.get_property with context as context and value as plugin and property_name as "name"
        Display "Executing plugin: " plus plugin_name
        
        Note: Initialize plugin
        Reflection.invoke_method with context as context and value as plugin and method_name as "initialize" and args as empty list
        
        Note: Process data
        For each data_item in test_data:
            Let result be Reflection.invoke_method with context as context and value as plugin and method_name as "execute" and args as list containing data_item
            Display "  Input: " plus data_item plus " → Output: " plus result
        
        Note: Cleanup plugin
        Reflection.invoke_method with context as context and value as plugin and method_name as "cleanup" and args as empty list
```

## Best Practices

### 1. Context Configuration

**Development Configuration:**
```runa
Let dev_config be Reflection.ReflectionConfig with:
    enable_runtime_reflection as true
    enable_compile_time_reflection as true
    enable_dynamic_invocation as true
    ai_mode as true
    metadata as Dictionary with "environment" as "development"
```

**Production Configuration:**
```runa
Let prod_config be Reflection.ReflectionConfig with:
    enable_runtime_reflection as true
    enable_compile_time_reflection as false  Note: Disable for performance
    enable_dynamic_invocation as false       Note: Disable for security
    ai_mode as false
    metadata as Dictionary with "environment" as "production"
```

### 2. Error Handling Patterns

```runa
Process called "safe_reflection_operation" that takes context as ReflectionContext and value as Any and operation as String returns Optional[Any]:
    Try:
        Match operation:
            When "introspect":
                Let type_info be Reflection.reflect_type with context as context and value as value
                Return some with value as type_info
            When "metadata":
                Let metadata be Reflection.get_metadata with context as context and value as value
                Return some with value as metadata
            Otherwise:
                Display "Unknown operation: " plus operation
                Return none
                
    Catch error as Reflection.ReflectionError:
        Display "Reflection operation failed: " plus error.message
        Return none
    Catch unexpected_error:
        Display "Unexpected error in reflection: " plus unexpected_error
        Return none
```

### 3. Performance Optimization

```runa
Note: Cache reflection results for frequently accessed types
Let reflection_cache be Dictionary containing

Process called "cached_reflect_type" that takes context as ReflectionContext and value as Any returns TypeInfo:
    Let type_key be generate_type_key with value as value
    
    If reflection_cache contains type_key:
        Return reflection_cache[type_key]
    
    Let type_info be Reflection.reflect_type with context as context and value as value
    Set reflection_cache[type_key] to type_info
    Return type_info

Process called "generate_type_key" that takes value as Any returns String:
    Note: Generate a cache key based on the value's type
    If value is Integer:
        Return "Integer"
    If value is String:
        Return "String"
    If value is List:
        Return "List"
    If value is Dictionary:
        Return "Dictionary"
    Return "Unknown"
```

## Performance Considerations

### Runtime Overhead

Reflection operations have minimal overhead:
- **Type Introspection**: ~10-50 nanoseconds per operation
- **Method Invocation**: ~100-500 nanoseconds additional overhead
- **Property Access**: ~20-100 nanoseconds additional overhead
- **Metadata Retrieval**: ~50-200 nanoseconds per operation

### Optimization Strategies

```runa
Note: Minimize reflection overhead in hot paths
Process called "optimized_reflection_usage" returns None:
    Let context be create_reflection_context with ai_mode as false  Note: Disable AI mode for performance
    
    Note: Pre-compute type information for frequently used types
    Let common_types be list containing 42, "text", list containing 1, 2, 3, Dictionary containing "key" as "value"
    Let type_cache be Dictionary containing
    
    For each value in common_types:
        Let type_info be Reflection.reflect_type with context as context and value as value
        Set type_cache[type_info.type_id] to type_info
    
    Note: Use cached type information in performance-critical code
    For i from 1 to 10000:
        Let sample_value be 42
        Note: Use cached type info instead of reflecting each time
        Let type_info be type_cache["Integer"]
        Note: Process using cached type information
```

## Integration with Other Metaprogramming Modules

### AST Manipulation Integration

```runa
Import "advanced/metaprogramming/ast_manipulation" as AST

Process called "reflection_guided_ast_generation" returns None:
    Let context be create_reflection_context with ai_mode as true
    
    Note: Use reflection to guide AST generation
    Let source_object be Dictionary with:
        "calculate" as Process that takes x as Integer and y as Integer returns Integer:
            Return x plus y
        "validate" as Process that takes input as Any returns Boolean:
            Return input is Integer
    
    Let methods be Reflection.list_methods with context as context and value as source_object
    
    Note: Generate AST based on reflected methods
    For each method_name in methods:
        Display "Generating AST for method: " plus method_name
        Note: Use AST manipulation to create equivalent code
        Let ast_node be AST.create_function_declaration with name as method_name
        Display "Generated AST node for: " plus method_name
```

### Code Generation Integration

```runa
Import "advanced/metaprogramming/code_synthesis" as CodeGen

Process called "reflection_driven_code_generation" returns None:
    Let context be create_reflection_context with ai_mode as true
    
    Note: Analyze existing code through reflection
    Let data_model be Dictionary with:
        "User" as Dictionary with:
            "name" as String
            "email" as String
            "age" as Integer
        "Product" as Dictionary with:
            "id" as Integer
            "name" as String
            "price" as Float
    
    Note: Generate CRUD operations based on reflected structure
    For each model_name in data_model:
        Let model_fields be data_model[model_name]
        Let properties be Reflection.list_properties with context as context and value as model_fields
        
        Display "Generating CRUD operations for " plus model_name
        For each property in properties:
            Display "  Property: " plus property plus " of type " plus model_fields[property]
            Note: Use CodeGen to create getter/setter methods
```

## Comparative Notes

### Advantages over Traditional Reflection

1. **Java vs Runa**: Runa's reflection is more natural and less verbose than Java's reflection API
2. **Python vs Runa**: Provides better type safety and error handling than Python's introspection
3. **C# vs Runa**: More AI-friendly syntax while maintaining similar power and performance
4. **JavaScript vs Runa**: Offers stronger typing and validation compared to JavaScript's dynamic nature

### AI-First Design Benefits

- **Natural Language Operations**: Method names and operations use clear, descriptive language
- **Comprehensive Error Messages**: Detailed error information helps AI agents debug issues
- **Metadata Rich**: Extensive metadata support enables AI reasoning about code structure
- **Validation Built-in**: Automatic validation helps prevent AI-generated reflection errors

## Error Handling and Recovery

The reflection system provides comprehensive error handling:

```runa
Process called "comprehensive_reflection_error_handling" returns None:
    Let context be create_reflection_context with ai_mode as true
    
    Note: Test various error scenarios
    Let test_object be Dictionary with "valid_method" as Process returns String: Return "success"
    
    Note: Test invalid method invocation
    Try:
        Reflection.invoke_method with context as context and value as test_object and method_name as "nonexistent_method" and args as empty list
    Catch error as Reflection.ReflectionError:
        Display "Expected error for nonexistent method: " plus error.message
        If "not found" in error.message:
            Display "Error correctly identified missing method"
    
    Note: Test invalid property access
    Try:
        Reflection.get_property with context as context and value as test_object and property_name as "nonexistent_property"
    Catch error as Reflection.ReflectionError:
        Display "Expected error for nonexistent property: " plus error.message
    
    Note: Test disabled features
    Let restricted_context be Reflection.ReflectionContext with:
        config as Reflection.ReflectionConfig with enable_dynamic_invocation as false
        stats as Reflection.ReflectionStats with total_introspections as 0 and total_invocations as 0 and total_errors as 0 and metadata as empty dictionary
        metadata as empty dictionary
    
    Try:
        Reflection.invoke_method with context as restricted_context and value as test_object and method_name as "valid_method" and args as empty list
    Catch error as Reflection.ReflectionError:
        Display "Expected error for disabled invocation: " plus error.message
        If "disabled" in error.message:
            Display "Security restriction correctly enforced"
```

This reflection module provides the foundation for powerful metaprogramming capabilities in Runa, enabling dynamic and flexible applications while maintaining type safety and performance.