# Runa Integration Documentation

This directory contains documentation about integrating Runa with other systems, embedding the Runa VM in applications, and interfacing with external libraries and languages.

## Overview

Runa is designed to be highly integrable with existing codebases and systems. This documentation covers various integration methods:

- **Embedding**: Adding Runa scripting capabilities to applications
- **FFI**: Calling native code from Runa programs
- **Language Interop**: Interfacing between Runa and other programming languages
- **Extensions**: Creating extensions and plugins for the Runa platform
- **Web Integration**: Using Runa in web applications and services

## Key Documents

- [Embedding RunaVM](Embedding_RunaVM.md) - Guide to embedding the Runa VM in applications
- [Foreign Function Interface](Foreign_Function_Interface.md) - Using the FFI to call native code
- [Native Libraries](Native_Libraries.md) - Working with native libraries in Runa
- [Language Interoperability](Language_Interoperability.md) - Interfacing with other programming languages
- [Web Integration](Web_Integration.md) - Using Runa in web environments

## Embedding RunaVM

The Runa VM can be embedded in applications written in various languages:

- **C/C++**: Direct integration using the C API
- **Python**: Via the Python binding module
- **JavaScript/Node.js**: Through the Node.js addon
- **Java**: Using the Java Native Interface (JNI) binding
- **C#/.NET**: Through P/Invoke and the .NET binding

Embedding allows you to:
- Add scripting capabilities to your application
- Create plugins and extensions in Runa
- Execute user-defined Runa code securely
- Dynamically modify application behavior

## Foreign Function Interface

The Runa FFI enables Runa code to:

- Call functions in native libraries (DLLs, SOs, DYLIBs)
- Work with C-compatible data structures
- Interface with operating system APIs
- Leverage performance-critical native code
- Integrate with existing systems and libraries

## Example: Embedding in C++

```cpp
#include <runavm.h>
#include <iostream>

int main() {
    // Create VM instance
    RunaVM* vm = runa_vm_create();
    
    // Register a C++ function
    auto print_func = [](RunaVM* vm, RunaValue* args, int arg_count) -> RunaValue {
        if (arg_count > 0 && runa_value_is_string(args[0])) {
            std::cout << "Message: " << runa_value_as_string(args[0]) << std::endl;
        }
        return runa_value_null();
    };
    
    runa_vm_register_function(vm, "print_message", print_func);
    
    // Load and run Runa code
    const char* script = 
        "Process called hello()\n"
        "    print_message(\"Hello from Runa!\")\n"
        "    Return 42\n"
        "End Process";
    
    runa_vm_load_string(vm, script, strlen(script));
    
    RunaValue result;
    runa_vm_call_function(vm, "hello", nullptr, 0, &result);
    
    if (runa_value_is_integer(result)) {
        std::cout << "Return value: " << runa_value_as_integer(result) << std::endl;
    }
    
    runa_value_release(&result);
    runa_vm_destroy(vm);
    
    return 0;
}
```

## Example: Using FFI in Runa

```
# Define an external library
External Library "libmath" with
    Windows = "math.dll",
    Linux = "libmath.so",
    MacOS = "libmath.dylib"
End

# Declare an external function
External Process called compute_sqrt(value as Float64) returns Float64 from "libmath"

# Use the external function
Process called main()
    Let x = 16.0
    Let result = compute_sqrt(x)
    Display "Square root of " + x.to_text() + " is " + result.to_text()
End Process
```

## Security Considerations

When integrating Runa, consider these security aspects:

- Use sandbox mode for untrusted code
- Apply appropriate resource limits
- Restrict filesystem and network access
- Validate all inputs before passing to native code
- Use memory-safe interfaces between languages

## Performance Tips

- Minimize data marshalling between Runa and host language
- Use bulk operations where possible
- Consider JIT compilation for performance-critical code
- Profile your integration points to identify bottlenecks
- Cache compiled Runa bytecode for repeated execution

## See Also

- [Runtime Documentation](../Runtime/README.md) - Information on the Runa runtime system
- [API Reference](../API/README.md) - API documentation for Runa libraries
- [Development Guide](../Development/README.md) - Resources for Runa language developers 