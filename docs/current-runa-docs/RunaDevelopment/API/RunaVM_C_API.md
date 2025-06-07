# RunaVM C API Reference

This document provides a comprehensive reference for the RunaVM C API, which allows embedding the Runa Virtual Machine in C and C++ applications.

## Table of Contents

1. [Overview](#overview)
2. [API Conventions](#api-conventions)
3. [VM Lifecycle](#vm-lifecycle)
4. [Code Execution](#code-execution)
5. [Memory Management](#memory-management)
6. [Error Handling](#error-handling)
7. [Value Management](#value-management)
8. [Function Registration](#function-registration)
9. [Type System](#type-system)
10. [Security Controls](#security-controls)
11. [Advanced Features](#advanced-features)
12. [Example Code](#example-code)

## Overview

The RunaVM C API provides a set of functions for integrating the Runa Virtual Machine into C/C++ applications. With this API, you can:

- Create and manage VM instances
- Load and execute Runa code
- Exchange data between C and Runa
- Register C functions for use from Runa
- Configure security and runtime options
- Handle errors and exceptions
- Access and manipulate Runa values

## API Conventions

### Header Files

```c
#include <runavm.h>           // Core VM functionality
#include <runavm_advanced.h>  // Advanced features (optional)
```

### Types

The API uses the following key types:

- `RunaVM*`: Opaque pointer to a VM instance
- `RunaValue`: Union type for all Runa values
- `RunaStatus`: Error code for API operations
- `RunaError`: Detailed error information
- `RunaFunction`: Function pointer for C callbacks

### Error Handling

Most functions return a `RunaStatus` code indicating success or failure:

```c
RunaStatus status = runa_vm_load_file(vm, "script.runa");
if (status != RUNA_SUCCESS) {
    // Handle error
}
```

### Thread Safety

Unless specified otherwise, API functions are not thread-safe. Use `runa_vm_create_thread_safe()` to create a thread-safe VM instance.

## VM Lifecycle

### Creating a VM

```c
// Create a basic VM instance
RunaVM* vm = runa_vm_create();

// Create a thread-safe VM instance
RunaVM* thread_safe_vm = runa_vm_create_thread_safe();

// Create a VM with custom memory configuration
RunaMemoryConfig mem_config = {
    .initial_heap_size = 64 * 1024 * 1024,  // 64 MB
    .max_heap_size = 512 * 1024 * 1024,     // 512 MB
    .gc_threshold = 75                      // Trigger GC at 75% heap usage
};
RunaVM* custom_vm = runa_vm_create_with_config(&mem_config);
```

### Destroying a VM

```c
runa_vm_destroy(vm);
```

### Configuration

```c
// Configure VM before use
runa_vm_set_memory_limit(vm, 100 * 1024 * 1024);  // 100 MB memory limit
runa_vm_enable_jit(vm, true);                     // Enable JIT compilation
runa_vm_set_library_path(vm, "/usr/lib/runa:/app/lib");
```

## Code Execution

### Loading Code

```c
// Load code from a file
RunaStatus status = runa_vm_load_file(vm, "script.runa");

// Load code from memory
const char* code = "Process called greet() Return \"Hello\" End Process";
status = runa_vm_load_string(vm, code, strlen(code));

// Load pre-compiled bytecode
status = runa_vm_load_bytecode(vm, bytecode);
```

### Executing Functions

```c
// Call a function with no arguments
RunaValue result;
status = runa_vm_call_function(vm, "main", NULL, 0, &result);

// Call a function with arguments
RunaValue args[2];
args[0] = runa_value_string("John");
args[1] = runa_value_integer(42);
status = runa_vm_call_function(vm, "greet", args, 2, &result);

// Process the result
if (status == RUNA_SUCCESS) {
    if (runa_value_is_string(result)) {
        printf("Result: %s\n", runa_value_as_string(result));
    }
    // Always release the result when done
    runa_value_release(&result);
}
```

### Evaluating Expressions

```c
RunaValue result;
status = runa_vm_eval(vm, "5 * 10 + 2", &result);
if (status == RUNA_SUCCESS) {
    printf("Result: %lld\n", runa_value_as_integer(result));
    runa_value_release(&result);
}
```

## Memory Management

### Reference Counting

RunaValue objects use reference counting for memory management:

```c
// Create a value
RunaValue text = runa_value_string("Example");

// Use the value
runa_vm_set_global(vm, "message", text);

// Release the value when done with it
runa_value_release(&text);
```

### Garbage Collection

```c
// Suggest garbage collection
runa_vm_collect_garbage(vm);

// Configure GC behavior
runa_vm_set_gc_threshold(vm, 70);  // Run GC when heap is 70% full
```

### Memory Pools

For performance-critical applications:

```c
// Create a memory pool
RunaMemoryPool* pool = runa_memory_pool_create(1024 * 1024);  // 1 MB pool

// Create a VM using the pool
RunaVM* vm = runa_vm_create_with_pool(pool);

// Use the VM normally
// ...

// Clean up
runa_vm_destroy(vm);
runa_memory_pool_destroy(pool);
```

## Error Handling

### Basic Error Handling

```c
RunaStatus status = runa_vm_call_function(vm, "process_data", args, 2, &result);
if (status != RUNA_SUCCESS) {
    printf("Error code: %d\n", status);
    printf("Error message: %s\n", runa_status_message(status));
}
```

### Detailed Error Information

```c
if (status != RUNA_SUCCESS) {
    RunaError error;
    runa_vm_get_last_error(vm, &error);
    
    printf("Error: %s\n", error.message);
    printf("Line: %d, Column: %d\n", error.line, error.column);
    printf("File: %s\n", error.file);
    printf("Stack trace:\n%s\n", error.stack_trace);
    
    runa_error_release(&error);
}
```

### Error Callback

```c
void on_error(RunaVM* vm, const RunaError* error, void* user_data) {
    printf("Runa error: %s at %s:%d\n", error->message, error->file, error->line);
    // Log the error to a file, etc.
}

// Register error callback
runa_vm_set_error_callback(vm, on_error, NULL);
```

## Value Management

### Creating Values

```c
RunaValue null_val = runa_value_null();
RunaValue bool_val = runa_value_boolean(true);
RunaValue int_val = runa_value_integer(42);
RunaValue dec_val = runa_value_decimal(3.14159);
RunaValue str_val = runa_value_string("Hello, World!");
```

### Creating Complex Values

```c
// Create a list
RunaValue list = runa_value_list(vm);
runa_list_append(list, runa_value_integer(1));
runa_list_append(list, runa_value_integer(2));
runa_list_append(list, runa_value_integer(3));

// Create a map
RunaValue map = runa_value_map(vm);
runa_map_set(map, runa_value_string("name"), runa_value_string("Alice"));
runa_map_set(map, runa_value_string("age"), runa_value_integer(30));
```

### Checking Value Types

```c
if (runa_value_is_integer(val)) {
    // Handle integer
} else if (runa_value_is_string(val)) {
    // Handle string
} else if (runa_value_is_list(val)) {
    // Handle list
}
```

### Converting Values

```c
// Get basic types
bool b = runa_value_as_boolean(val);
int64_t i = runa_value_as_integer(val);
double d = runa_value_as_decimal(val);
const char* s = runa_value_as_string(val);

// Check for null
bool is_null = runa_value_is_null(val);
```

### Working with Lists

```c
RunaValue list = /* get list from somewhere */;
size_t len = runa_list_length(list);

// Iterate through list
for (size_t i = 0; i < len; i++) {
    RunaValue item;
    runa_list_get(list, i, &item);
    
    // Process item
    if (runa_value_is_integer(item)) {
        printf("Item %zu: %lld\n", i, runa_value_as_integer(item));
    }
    
    runa_value_release(&item);
}

// Add to list
runa_list_append(list, runa_value_string("new item"));
```

### Working with Maps

```c
RunaValue map = /* get map from somewhere */;

// Get a value from the map
RunaValue name;
if (runa_map_get(map, runa_value_string("name"), &name) == RUNA_SUCCESS) {
    printf("Name: %s\n", runa_value_as_string(name));
    runa_value_release(&name);
}

// Set a value in the map
runa_map_set(map, runa_value_string("count"), runa_value_integer(42));

// Check if key exists
bool has_age = runa_map_has_key(map, runa_value_string("age"));

// Get all keys
RunaValue keys;
runa_map_keys(map, &keys);
// ... process keys list ...
runa_value_release(&keys);
```

## Function Registration

### Basic Function Registration

```c
// Define a C function to be called from Runa
RunaValue hello_world(RunaVM* vm, RunaValue* args, int arg_count) {
    printf("Hello from C!\n");
    
    if (arg_count > 0 && runa_value_is_string(args[0])) {
        printf("Argument: %s\n", runa_value_as_string(args[0]));
    }
    
    return runa_value_string("Greeting complete");
}

// Register the function
runa_vm_register_function(vm, "hello_world", hello_world);
```

### Function with User Data

```c
typedef struct {
    FILE* log_file;
    int log_level;
} LogContext;

RunaValue log_message(RunaVM* vm, RunaValue* args, int arg_count, void* user_data) {
    LogContext* ctx = (LogContext*)user_data;
    
    if (arg_count > 0 && runa_value_is_string(args[0])) {
        fprintf(ctx->log_file, "LOG [%d]: %s\n", 
                ctx->log_level, runa_value_as_string(args[0]));
    }
    
    return runa_value_null();
}

// Create context
LogContext* ctx = malloc(sizeof(LogContext));
ctx->log_file = fopen("app.log", "a");
ctx->log_level = 1;

// Register with context
runa_vm_register_function_with_data(vm, "log_message", log_message, ctx);
```

### Module Registration

```c
// Register a group of functions as a module
RunaStatus register_file_module(RunaVM* vm) {
    runa_vm_begin_module(vm, "file");
    
    runa_vm_register_function(vm, "read", file_read);
    runa_vm_register_function(vm, "write", file_write);
    runa_vm_register_function(vm, "exists", file_exists);
    runa_vm_register_function(vm, "delete", file_delete);
    
    return runa_vm_end_module(vm);
}

// Later, use the module in Runa code:
// Import file from "file"
// Let content = file.read("example.txt")
```

## Type System

### Creating Custom Types

```c
// Define a struct for the custom type
typedef struct {
    char* name;
    int age;
} Person;

// Destructor function
void person_destroy(void* data) {
    Person* person = (Person*)data;
    free(person->name);
    free(person);
}

// Register the type
RunaTypeID person_type = runa_vm_register_type(vm, "Person", person_destroy);

// Create a value of the custom type
Person* person = malloc(sizeof(Person));
person->name = strdup("Alice");
person->age = 30;

RunaValue person_val = runa_value_custom(person_type, person);
```

### Type Checking

```c
// Check if value is of a specific type
bool is_person = runa_value_is_type(val, person_type);

// Get type information
RunaTypeID type_id = runa_value_get_type(val);
const char* type_name = runa_type_get_name(vm, type_id);
printf("Value is of type: %s\n", type_name);
```

### Method Registration

```c
// Method to get a person's name
RunaValue person_get_name(RunaVM* vm, RunaValue* args, int arg_count) {
    if (arg_count < 1 || !runa_value_is_type(args[0], person_type)) {
        return runa_value_null();
    }
    
    Person* person = (Person*)runa_value_get_custom_data(args[0]);
    return runa_value_string(person->name);
}

// Register the method
runa_vm_register_method(vm, person_type, "get_name", person_get_name);

// In Runa:
// Let p = Person("Alice", 30)
// Let name = p.get_name()  // "Alice"
```

## Security Controls

### Sandboxing

```c
// Enable sandbox mode
runa_vm_enable_sandbox(vm, true);

// Configure sandbox permissions
runa_vm_set_permission(vm, RUNA_PERMISSION_FILESYSTEM, RUNA_ACCESS_READ);
runa_vm_set_permission(vm, RUNA_PERMISSION_NETWORK, RUNA_ACCESS_NONE);
runa_vm_set_permission(vm, RUNA_PERMISSION_SYSTEM, RUNA_ACCESS_NONE);
runa_vm_set_permission(vm, RUNA_PERMISSION_PROCESS, RUNA_ACCESS_NONE);
```

### Resource Limits

```c
// Set execution limits
runa_vm_set_memory_limit(vm, 50 * 1024 * 1024);  // 50 MB
runa_vm_set_execution_timeout(vm, 5000);         // 5 seconds
runa_vm_set_instruction_limit(vm, 10000000);     // 10M instructions

// Allow specific filesystem access
runa_vm_allow_filesystem_path(vm, "/tmp", RUNA_ACCESS_READ_WRITE);
runa_vm_allow_filesystem_path(vm, "/home/user/data", RUNA_ACCESS_READ);
```

### Security Policies

```c
// Load a security policy from a file
runa_vm_load_security_policy(vm, "security_policy.json");

// Or configure programmatically
runa_vm_begin_security_policy(vm);
runa_vm_add_policy_rule(vm, "filesystem", "allow", "/tmp", "read_write");
runa_vm_add_policy_rule(vm, "network", "allow", "localhost:8080", "connect");
runa_vm_end_security_policy(vm);
```

## Advanced Features

### Debugging

```c
// Enable debugging capabilities
runa_vm_enable_debugging(vm, true);

// Set debugger hooks
runa_vm_set_debug_hook(vm, RUNA_DEBUG_LINE, debug_line_hook);
runa_vm_set_debug_hook(vm, RUNA_DEBUG_CALL, debug_call_hook);

// Enable remote debugging
runa_vm_enable_remote_debugging(vm, "localhost", 8089);
```

### Profiling

```c
// Start CPU profiling
runa_vm_start_profile(vm, RUNA_PROFILE_CPU, "cpu_profile.json");

// Execute code...

// Stop profiling
runa_vm_stop_profile(vm, RUNA_PROFILE_CPU);

// Memory profiling
runa_vm_start_profile(vm, RUNA_PROFILE_MEMORY, "memory_profile.json");
// ...
runa_vm_stop_profile(vm, RUNA_PROFILE_MEMORY);

// Allocation tracking
runa_vm_start_profile(vm, RUNA_PROFILE_ALLOCATIONS, "allocations.json");
// ...
runa_vm_stop_profile(vm, RUNA_PROFILE_ALLOCATIONS);
```

### JIT Compilation

```c
// Enable JIT with default settings
runa_vm_enable_jit(vm, true);

// Configure JIT behavior
runa_vm_set_jit_threshold(vm, 1000);  // Compile functions executed 1000+ times
runa_vm_set_jit_optimization_level(vm, 2);  // Optimization level (0-3)
```

### Multithreading Support

```c
// Create a thread-safe VM
RunaVM* vm = runa_vm_create_thread_safe();

// Create a mutex
RunaMutex* mutex = runa_mutex_create();

// Lock and unlock
runa_mutex_lock(mutex);
// Critical section...
runa_mutex_unlock(mutex);

// Clean up
runa_mutex_destroy(mutex);
```

## Example Code

### Basic Embedding Example

```c
#include <runavm.h>
#include <stdio.h>

int main() {
    // Create a VM instance
    RunaVM* vm = runa_vm_create();
    if (!vm) {
        fprintf(stderr, "Failed to create RunaVM\n");
        return 1;
    }
    
    // Define a C function to register
    RunaValue print_func(RunaVM* vm, RunaValue* args, int arg_count) {
        if (arg_count > 0 && runa_value_is_string(args[0])) {
            printf("From Runa: %s\n", runa_value_as_string(args[0]));
        }
        return runa_value_null();
    }
    
    // Register the function
    runa_vm_register_function(vm, "print_message", print_func);
    
    // Load a script
    const char* script = 
        "Process called hello(name as Text) returns Text\n"
        "    print_message(\"Hello, \" + name)\n"
        "    Return \"Greeting sent to \" + name\n"
        "End Process";
    
    RunaStatus status = runa_vm_load_string(vm, script, strlen(script));
    if (status != RUNA_SUCCESS) {
        RunaError error;
        runa_vm_get_last_error(vm, &error);
        fprintf(stderr, "Failed to load script: %s\n", error.message);
        runa_error_release(&error);
        runa_vm_destroy(vm);
        return 1;
    }
    
    // Call the function
    RunaValue arg = runa_value_string("World");
    RunaValue result;
    
    status = runa_vm_call_function(vm, "hello", &arg, 1, &result);
    runa_value_release(&arg);
    
    if (status != RUNA_SUCCESS) {
        RunaError error;
        runa_vm_get_last_error(vm, &error);
        fprintf(stderr, "Failed to call function: %s\n", error.message);
        runa_error_release(&error);
    } else {
        if (runa_value_is_string(result)) {
            printf("Result: %s\n", runa_value_as_string(result));
        }
        runa_value_release(&result);
    }
    
    // Clean up
    runa_vm_destroy(vm);
    return 0;
}
```

### Advanced Example: Plugin System

```c
// See the more complex example in the Embedding RunaVM guide
```

---

For more detailed information, examples, and advanced topics, please refer to the [Embedding RunaVM Guide](../Integration/Embedding_RunaVM.md) and the [RunaVM Architecture Documentation](../Runtime/RunaVM.md). 