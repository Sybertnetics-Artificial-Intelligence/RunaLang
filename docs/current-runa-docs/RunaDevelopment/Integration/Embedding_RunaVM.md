# Embedding RunaVM in Applications

This guide covers how to embed the Runa Virtual Machine (RunaVM) into other applications, allowing you to add Runa scripting capabilities to your software.

## Table of Contents

1. [Overview](#overview)
2. [Integration Options](#integration-options)
3. [C/C++ Integration](#cc-integration)
4. [Python Integration](#python-integration)
5. [JavaScript/Node.js Integration](#javascriptnodejs-integration)
6. [Java Integration](#java-integration)
7. [Configuration Options](#configuration-options)
8. [Security Considerations](#security-considerations)
9. [Memory Management](#memory-management)
10. [Performance Optimization](#performance-optimization)
11. [Debugging Embedded Runa](#debugging-embedded-runa)
12. [Best Practices](#best-practices)
13. [Examples](#examples)
14. [References](#references)

## Overview

Embedding RunaVM allows you to:

- Add scripting capabilities to your application
- Create user-extensible plugins in Runa
- Execute user-provided Runa code in a sandboxed environment
- Dynamically load and run Runa modules

The RunaVM embedding API provides a clean interface to load, execute, and interact with Runa code from your host application.

## Integration Options

RunaVM offers multiple integration paths depending on your application's requirements:

### Static Linking

- Complete VM integrated directly into your application
- No external dependencies required
- Maximum control over VM lifecycle

### Dynamic Linking

- Load the RunaVM library at runtime
- Smaller binary size for your application
- Can update VM independently of your application

### Service Integration

- Communicate with a separately running RunaVM process
- Minimal memory footprint in your application
- Process isolation for enhanced security

## C/C++ Integration

### Prerequisites

- RunaVM development headers (`runavm.h`)
- RunaVM shared or static library

### Basic Integration

1. Include the RunaVM header:

```c
#include <runavm.h>
```

2. Create a VM instance:

```c
RunaVM* vm = runa_vm_create();
if (!vm) {
    fprintf(stderr, "Failed to create RunaVM instance\n");
    return 1;
}
```

3. Load and run Runa code:

```c
// Load from file
RunaStatus status = runa_vm_load_file(vm, "script.runa");
if (status != RUNA_SUCCESS) {
    fprintf(stderr, "Failed to load script: %s\n", runa_status_message(status));
    runa_vm_destroy(vm);
    return 1;
}

// Execute main function
RunaValue result;
status = runa_vm_call_function(vm, "main", NULL, 0, &result);
if (status != RUNA_SUCCESS) {
    fprintf(stderr, "Failed to execute: %s\n", runa_status_message(status));
}

// Clean up result if needed
runa_value_release(&result);
```

4. Clean up:

```c
runa_vm_destroy(vm);
```

### Exposing Host Functions to Runa

Register C functions to be callable from Runa code:

```c
// Function to be called from Runa
RunaValue host_log(RunaVM* vm, RunaValue* args, int arg_count) {
    if (arg_count > 0 && runa_value_is_string(args[0])) {
        const char* message = runa_value_as_string(args[0]);
        printf("Runa Log: %s\n", message);
    }
    return runa_value_null();
}

// Register the function
runa_vm_register_function(vm, "host_log", host_log);
```

### Accessing Runa Values from C

Working with Runa data types in C:

```c
// Get a global variable from Runa
RunaValue config;
status = runa_vm_get_global(vm, "CONFIG", &config);
if (status == RUNA_SUCCESS) {
    if (runa_value_is_map(config)) {
        RunaValue port_value;
        status = runa_map_get(config, "port", &port_value);
        if (status == RUNA_SUCCESS && runa_value_is_integer(port_value)) {
            int port = runa_value_as_integer(port_value);
            printf("Port from Runa: %d\n", port);
            runa_value_release(&port_value);
        }
    }
    runa_value_release(&config);
}
```

## Python Integration

RunaVM provides a Python package for easy integration.

### Installation

```bash
pip install runavm
```

### Basic Usage

```python
import runavm

# Create a VM instance
vm = runavm.VM()

# Load Runa code from string
vm.load_string("""
Process called greet(name as Text) returns Text
    Return "Hello, " + name + "!"
End Process
""")

# Call a Runa function
result = vm.call_function("greet", ["World"])
print(result)  # Output: Hello, World!

# Evaluate an expression
result = vm.eval("5 * 10 + 2")
print(result)  # Output: 52
```

### Exposing Python Functions to Runa

```python
def py_calculate_distance(x1, y1, x2, y2):
    import math
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Register the function
vm.register_function("calculate_distance", py_calculate_distance)

# Now you can call it from Runa code
vm.load_string("""
Process called find_distance() returns Decimal
    Return calculate_distance(0, 0, 3, 4)
End Process
""")

result = vm.call_function("find_distance")
print(result)  # Output: 5.0
```

## JavaScript/Node.js Integration

For web and Node.js applications, use the RunaVM JavaScript package.

### Installation

```bash
npm install runavm
```

### Basic Usage

```javascript
const runavm = require('runavm');

// Create a VM instance
const vm = new runavm.VM();

// Load Runa code
vm.loadString(`
Process called fibonacci(n as Integer) returns Integer
    If n <= 1
        Return n
    End If
    Return fibonacci(n - 1) + fibonacci(n - 2)
End Process
`);

// Call Runa function
const result = vm.callFunction('fibonacci', [10]);
console.log(result);  // Output: 55

// Evaluate expressions
const value = vm.eval('List of Integer(1, 2, 3).map(x => x * 2)');
console.log(value);  // Output: [2, 4, 6]
```

### Exposing JavaScript Functions to Runa

```javascript
// Define a JavaScript function
function fetchData(url) {
    return fetch(url)
        .then(response => response.json())
        .catch(error => ({ error: error.message }));
}

// Register the function
vm.registerFunction('fetch_data', fetchData);

// Use the function in Runa code
vm.loadString(`
Process called get_user_data(id as Integer) returns Map
    Return fetch_data("https://api.example.com/users/" + id.to_text())
End Process
`);
```

## Java Integration

For Java applications, use the RunaVM Java library.

### Maven Dependency

```xml
<dependency>
    <groupId>org.runalang</groupId>
    <artifactId>runavm</artifactId>
    <version>1.0.0</version>
</dependency>
```

### Basic Usage

```java
import org.runalang.VM;
import org.runalang.RunaValue;
import org.runalang.RunaException;

public class RunaDemo {
    public static void main(String[] args) {
        try {
            // Create a VM instance
            VM vm = new VM();
            
            // Load Runa code from file
            vm.loadFile("script.runa");
            
            // Call a function
            RunaValue result = vm.callFunction("process_data", 
                VM.createString("sample"), VM.createInteger(42));
            
            System.out.println(result.asString());
            
        } catch (RunaException e) {
            System.err.println("Runa error: " + e.getMessage());
        }
    }
}
```

### Exposing Java Methods to Runa

```java
import org.runalang.VM;
import org.runalang.RunaValue;
import org.runalang.RunaFunction;

public class DatabaseAccess {
    // Java method to be exposed to Runa
    public static RunaValue queryDatabase(RunaValue[] args) {
        if (args.length < 1 || !args[0].isString()) {
            return VM.createNull();
        }
        
        String query = args[0].asString();
        // Execute database query...
        
        // Return results as a Runa Map
        return VM.createMap("status", VM.createString("success"),
                           "count", VM.createInteger(results.size()));
    }
    
    public static void registerFunctions(VM vm) {
        vm.registerFunction("query_db", DatabaseAccess::queryDatabase);
    }
}
```

## Configuration Options

When embedding RunaVM, configure it to meet your application's needs:

### Memory Limits

```c
// C API example
runa_vm_set_memory_limit(vm, 100 * 1024 * 1024); // 100 MB
```

```python
# Python example
vm.set_config("memory_limit", 100 * 1024 * 1024)  # 100 MB
```

### Execution Timeout

```c
// C API example
runa_vm_set_execution_timeout(vm, 5000); // 5 seconds
```

```javascript
// JavaScript example
vm.setConfig("execution_timeout", 5000);  // 5 seconds
```

### Library Access

```c
// C API example
runa_vm_set_library_path(vm, "/app/libs:/usr/lib/runa");
```

```java
// Java example
vm.setConfig("library_path", "/app/libs:/usr/lib/runa");
```

### JIT Compilation

```c
// C API example
runa_vm_enable_jit(vm, true);
```

## Security Considerations

When embedding RunaVM, consider these security practices:

### Sandboxing

Restrict access to system resources:

```c
// C API example
runa_vm_enable_sandbox(vm, true);
runa_vm_set_permission(vm, RUNA_PERMISSION_FILESYSTEM, RUNA_ACCESS_NONE);
runa_vm_set_permission(vm, RUNA_PERMISSION_NETWORK, RUNA_ACCESS_NONE);
```

### Resource Limits

Prevent resource exhaustion:

```c
// C API example
runa_vm_set_memory_limit(vm, 50 * 1024 * 1024); // 50 MB memory limit
runa_vm_set_instruction_limit(vm, 10000000); // 10M instruction limit
```

### Input Validation

Always validate Runa code before execution:

```c
// C API example
RunaStatus status = runa_vm_validate(vm, code, code_length);
if (status != RUNA_SUCCESS) {
    // Handle invalid code
}
```

## Memory Management

When working with RunaVM in memory-sensitive applications:

### Reference Counting

The C API uses reference counting for RunaValue objects:

```c
RunaValue value = runa_value_string("example");
// ... use value ...
runa_value_release(&value); // Decrements reference count
```

### Garbage Collection Hints

Suggest when garbage collection should run:

```c
// C API example
runa_vm_collect_garbage(vm); // Force garbage collection
```

```python
# Python example
vm.collect_garbage()
```

### Memory Pools

For high-performance applications, use memory pools:

```c
// C API example
RunaMemoryPool* pool = runa_memory_pool_create(1024 * 1024); // 1 MB pool
RunaVM* vm = runa_vm_create_with_pool(pool);

// ... use VM ...

runa_vm_destroy(vm);
runa_memory_pool_destroy(pool);
```

## Performance Optimization

Maximize performance when embedding RunaVM:

### Pre-Compilation

Compile Runa code ahead of time:

```c
// C API example
RunaBytecode* bytecode = runa_compile_file("script.runa");
if (bytecode) {
    runa_vm_load_bytecode(vm, bytecode);
    runa_bytecode_release(bytecode);
}
```

### Module Caching

Cache compiled modules for reuse:

```c
// C API pseudocode
RunaModule* cached_module = get_from_cache("module_name");
if (!cached_module) {
    cached_module = runa_vm_compile_module(vm, "module_name");
    add_to_cache("module_name", cached_module);
}
runa_vm_load_module_from_memory(vm, cached_module);
```

### Thread Management

For multi-threaded applications:

```c
// C API example - create a thread-safe VM
RunaVM* vm = runa_vm_create_thread_safe();

// Or create thread-local VMs
// In thread 1:
RunaVM* vm1 = runa_vm_create();
// In thread 2:
RunaVM* vm2 = runa_vm_create();
```

## Debugging Embedded Runa

Debug Runa code running in your application:

### Error Handling

```c
// C API example
RunaStatus status = runa_vm_call_function(vm, "process_data", NULL, 0, &result);
if (status != RUNA_SUCCESS) {
    RunaError error;
    runa_vm_get_last_error(vm, &error);
    
    printf("Error: %s\n", error.message);
    printf("Line: %d, Column: %d\n", error.line, error.column);
    printf("Stack trace:\n%s\n", error.stack_trace);
    
    runa_error_release(&error);
}
```

### Debug Hooks

Register debug callbacks:

```c
// C API example
void on_line_executed(RunaVM* vm, const char* file, int line) {
    printf("Executing %s:%d\n", file, line);
}

runa_vm_set_debug_hook(vm, RUNA_DEBUG_LINE, on_line_executed);
```

### External Debugger Connection

Enable remote debugging:

```c
// C API example
runa_vm_enable_remote_debugging(vm, "localhost", 8089);
```

## Best Practices

### Resource Management

- Always clean up VM instances when done
- Be careful with cross-language references
- Use appropriate memory limits for your application

### Error Handling

- Always check return status from API calls
- Provide useful error information to users
- Consider using try/catch in host language

### Threading Considerations

- Use thread-safe VM instances for shared access
- Create separate VMs per thread when possible
- Be careful with concurrent access to shared resources

### Versioning

- Handle RunaVM version compatibility
- Check for feature availability at runtime
- Ensure consistent VM version across deployments

## Examples

### Simple Scripting Engine

```c
#include <runavm.h>
#include <stdio.h>

int main(int argc, char** argv) {
    if (argc < 2) {
        printf("Usage: %s <script.runa>\n", argv[0]);
        return 1;
    }
    
    RunaVM* vm = runa_vm_create();
    if (!vm) {
        fprintf(stderr, "Failed to create VM\n");
        return 1;
    }
    
    // Configure VM
    runa_vm_set_memory_limit(vm, 50 * 1024 * 1024); // 50MB
    runa_vm_enable_jit(vm, true);
    
    // Load script
    RunaStatus status = runa_vm_load_file(vm, argv[1]);
    if (status != RUNA_SUCCESS) {
        RunaError error;
        runa_vm_get_last_error(vm, &error);
        fprintf(stderr, "Failed to load script: %s\n", error.message);
        runa_error_release(&error);
        runa_vm_destroy(vm);
        return 1;
    }
    
    // Execute main function
    RunaValue result;
    status = runa_vm_call_function(vm, "main", NULL, 0, &result);
    if (status != RUNA_SUCCESS) {
        RunaError error;
        runa_vm_get_last_error(vm, &error);
        fprintf(stderr, "Error: %s\n", error.message);
        runa_error_release(&error);
    } else {
        if (runa_value_is_integer(result)) {
            printf("Result: %lld\n", runa_value_as_integer(result));
        } else if (runa_value_is_string(result)) {
            printf("Result: %s\n", runa_value_as_string(result));
        } else {
            printf("Function executed successfully\n");
        }
        runa_value_release(&result);
    }
    
    runa_vm_destroy(vm);
    return 0;
}
```

### Plugin System Example

```c++
// C++ Plugin System Example
#include <runavm.h>
#include <string>
#include <map>
#include <vector>

class PluginSystem {
private:
    RunaVM* vm;
    std::map<std::string, RunaValue> registered_callbacks;
    
public:
    PluginSystem() {
        vm = runa_vm_create();
        runa_vm_enable_sandbox(vm, true);
        runa_vm_set_permission(vm, RUNA_PERMISSION_FILESYSTEM, RUNA_ACCESS_READ);
        runa_vm_set_memory_limit(vm, 20 * 1024 * 1024); // 20MB
        
        // Register host API
        runa_vm_register_function(vm, "register_callback", registerCallbackHandler);
        runa_vm_register_function(vm, "log_message", logMessageHandler);
    }
    
    ~PluginSystem() {
        // Clean up callbacks
        for (auto& pair : registered_callbacks) {
            runa_value_release(&pair.second);
        }
        
        runa_vm_destroy(vm);
    }
    
    bool loadPlugin(const std::string& filename) {
        RunaStatus status = runa_vm_load_file(vm, filename.c_str());
        return status == RUNA_SUCCESS;
    }
    
    bool executeCallback(const std::string& name, const std::vector<RunaValue>& args) {
        auto it = registered_callbacks.find(name);
        if (it == registered_callbacks.end()) {
            return false;
        }
        
        RunaStatus status = runa_vm_call_value(vm, it->second, 
                                             args.data(), args.size(), NULL);
        return status == RUNA_SUCCESS;
    }
    
    static RunaValue registerCallbackHandler(RunaVM* vm, RunaValue* args, int arg_count) {
        if (arg_count < 2 || !runa_value_is_string(args[0]) || !runa_value_is_function(args[1])) {
            return runa_value_boolean(false);
        }
        
        const char* name = runa_value_as_string(args[0]);
        
        // Get the plugin system instance from user data
        PluginSystem* system = (PluginSystem*)runa_vm_get_user_data(vm);
        
        // Store the callback function
        RunaValue callback = runa_value_copy(args[1]);
        
        // Remove old callback if exists
        auto it = system->registered_callbacks.find(name);
        if (it != system->registered_callbacks.end()) {
            runa_value_release(&it->second);
            system->registered_callbacks.erase(it);
        }
        
        system->registered_callbacks[name] = callback;
        return runa_value_boolean(true);
    }
    
    static RunaValue logMessageHandler(RunaVM* vm, RunaValue* args, int arg_count) {
        if (arg_count > 0 && runa_value_is_string(args[0])) {
            printf("Plugin Log: %s\n", runa_value_as_string(args[0]));
        }
        return runa_value_null();
    }
    
    void initialize() {
        runa_vm_set_user_data(vm, this);
        
        // Execute initialization
        RunaStatus status = runa_vm_call_function(vm, "initialize", NULL, 0, NULL);
        if (status != RUNA_SUCCESS) {
            RunaError error;
            runa_vm_get_last_error(vm, &error);
            printf("Initialization error: %s\n", error.message);
            runa_error_release(&error);
        }
    }
};
```

## References

- [RunaVM C API Reference](../API/RunaVM_C_API.md)
- [Foreign Function Interface Guide](Foreign_Function_Interface.md)
- [Security Best Practices](../Security/Sandboxing.md)
- [Performance Tuning Guide](../Performance/Optimization.md) 