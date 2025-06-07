# Foreign Function Interface (FFI)

The Runa Foreign Function Interface (FFI) provides a mechanism for Runa code to interact with native libraries and functions written in languages like C, C++, Rust, and others. This document covers the concepts, syntax, and best practices for using FFI in Runa applications.

## Table of Contents

1. [Overview](#overview)
2. [Basic Concepts](#basic-concepts)
3. [Declaring External Libraries](#declaring-external-libraries)
4. [Calling External Functions](#calling-external-functions)
5. [Data Type Mapping](#data-type-mapping)
6. [Memory Management](#memory-management)
7. [Callback Functions](#callback-functions)
8. [Structs and Unions](#structs-and-unions)
9. [Error Handling](#error-handling)
10. [Platform Considerations](#platform-considerations)
11. [Security Best Practices](#security-best-practices)
12. [Performance Optimizations](#performance-optimizations)
13. [Examples](#examples)
14. [References](#references)

## Overview

Runa's FFI system allows seamless integration with native code, enabling you to:

- Access operating system APIs
- Utilize existing native libraries
- Implement performance-critical components in native languages
- Bridge Runa applications with legacy systems
- Create extensible applications with native plugins

The FFI is designed to be both powerful and safe, with strong type checking, automated memory management, and configurable security controls.

## Basic Concepts

### The FFI Bridge

The Runa FFI bridge handles:

- Loading native shared libraries (DLLs, SO files, DYLIBs)
- Marshalling data between Runa and native code
- Managing memory and resource lifecycles
- Providing error handling for native function calls

### FFI Architecture

```
┌───────────────────────────────────────┐
│           Runa Application            │
└───────────────────────────────────────┘
                    │
┌───────────────────────────────────────┐
│              FFI Bridge               │
│                                       │
│  ┌─────────────┐     ┌─────────────┐  │
│  │   Type      │     │  Function   │  │
│  │ Conversion  │     │  Resolver   │  │
│  └─────────────┘     └─────────────┘  │
│                                       │
│  ┌─────────────┐     ┌─────────────┐  │
│  │  Memory     │     │  Library    │  │
│  │ Management  │     │   Loader    │  │
│  └─────────────┘     └─────────────┘  │
└───────────────────────────────────────┘
                    │
┌───────────────────────────────────────┐
│        Native Code / Libraries        │
└───────────────────────────────────────┘
```

## Declaring External Libraries

Before using external functions, you must declare the library containing them:

```
# Basic library declaration
External Library "libc"

# Platform-specific library paths
External Library "math" with
    Windows = "math.dll",
    Linux = "libmath.so",
    MacOS = "libmath.dylib"
End

# Library with specific version
External Library "sqlite3" version "3.34.0"
```

### Library Search Path

Libraries are searched in the following order:

1. Current directory
2. Runa application directory
3. Standard system library paths
4. Paths specified in `RUNA_LIBRARY_PATH` environment variable

You can also specify absolute paths:

```
External Library "/usr/local/lib/libcustom.so"
```

## Calling External Functions

### Basic Function Declaration

To use an external function, declare it with the `External Process` syntax:

```
# Basic external function declaration
External Process called printf(format as Pointer, args as Any) returns Integer from "libc"

# Using the function
Process called print_message()
    Let message = "Hello from Runa!\n"
    printf(message.to_c_string(), Null)
End Process
```

### Function Naming

If the external function name differs from what you want to use in Runa:

```
External Process called file_exists(path as Pointer) returns Integer 
    from "libc" as "access"
```

### Calling Conventions

Specify non-default calling conventions when needed:

```
External Process called win_api_function(handle as Integer, message as Pointer) returns Integer 
    from "user32" 
    with calling_convention = "stdcall"
```

Available calling conventions:
- `cdecl` (default)
- `stdcall`
- `fastcall`
- `thiscall` (C++ only)

## Data Type Mapping

### Basic Type Mappings

| Runa Type | C/Native Type   | Notes                                   |
|-----------|-----------------|----------------------------------------|
| Integer   | int, long       | Size depends on platform architecture   |
| Decimal   | double          | 64-bit floating point                   |
| Boolean   | int (0/1)       | Converted to int for C compatibility    |
| Text      | char*           | Use `to_c_string()` for conversion      |
| Byte      | unsigned char   | 8-bit unsigned integer                  |
| Pointer   | void*           | Raw memory address                      |
| Struct    | struct          | User-defined structure mapping          |

### Explicit Type Sizes

When precise sizes are needed:

```
External Process called read_data(buffer as Pointer, size as Int32) returns Int32 from "libc"
```

Available precise types:
- `Int8`, `Int16`, `Int32`, `Int64`
- `UInt8`, `UInt16`, `UInt32`, `UInt64`
- `Float32`, `Float64`

### Working with Text

Converting between Runa Text and C strings:

```
# Runa to C string
Let name = "Alice"
Let c_name = name.to_c_string()  # Returns a Pointer

# C string to Runa
Let message_ptr = get_error_message()  # Returns char* as Pointer
Let message = Text.from_c_string(message_ptr)
```

### Arrays

Working with C arrays:

```
# Declare a function accepting an array
External Process called process_data(data as Pointer, length as Integer) returns Integer from "data_lib"

# Create an array and pass it
Process called analyze()
    Let values = [1, 2, 3, 4, 5]
    Let array_ptr = values.to_c_array(Int32)  # Create typed C array
    Let result = process_data(array_ptr, values.length())
    array_ptr.free()  # Clean up when done
End Process
```

## Memory Management

### Allocation and Deallocation

```
# Allocate memory
Let buffer = Memory.allocate(1024)  # Allocate 1024 bytes, returns Pointer

# Use the memory for a C function
read_file("/path/to/file", buffer, 1024)

# Free the memory when done
buffer.free()
```

### Automatic Memory Management

Use `with` blocks for automatic cleanup:

```
Process called read_config(path as Text) returns Map
    with Memory.allocate(4096) as buffer
        Let bytes_read = read_file(path.to_c_string(), buffer, 4096)
        Return parse_config_data(buffer, bytes_read)
    End with  # buffer is automatically freed
End Process
```

### Reference Counting

Some FFI objects use reference counting:

```
Let lib_handle = Library.load("graphics")
# ...use the library...
lib_handle.unref()  # Decrease reference count
```

## Callback Functions

### Defining Callbacks

Pass Runa functions to native code:

```
# Declare a native function that accepts a callback
External Process called set_data_processor(
    callback as Pointer, 
    user_data as Pointer
) returns Integer from "processor_lib"

# Create a callback function
Process called process_item(item as Pointer, size as Integer) returns Integer
    # Process the data
    Let data = Memory.read_bytes(item, size)
    Let result = analyze_data(data)
    Return result
End Process

# Register the callback
Process called setup_processing()
    Let callback_ptr = FFI.create_callback(process_item)
    set_data_processor(callback_ptr, Null)
    # The callback remains valid until the program exits
    # or callback_ptr.release() is called
End Process
```

### Callback Lifetime

Callbacks must remain valid as long as the native code might call them:

```
Let callback_ptr = FFI.create_callback(my_callback)
set_callback(callback_ptr)

# Later, when no longer needed:
callback_ptr.release()
```

## Structs and Unions

### Defining Structs

```
# Define a struct matching a C struct
FFI Structure Point with
    x as Int32,
    y as Int32
End Structure

# Using the struct
Process called draw_point(x as Integer, y as Integer)
    Let point = Point()
    point.x = x
    point.y = y
    
    render_point(point.to_pointer())
End Process
```

### Nested Structures

```
FFI Structure Rectangle with
    top_left as Point,
    bottom_right as Point
End Structure
```

### Arrays in Structures

```
FFI Structure ColorRGB with
    components as Array of Byte(3)  # [r, g, b]
End Structure
```

### Unions

```
FFI Union Value with
    as_int as Int32,
    as_float as Float32,
    as_pointer as Pointer
End Union
```

## Error Handling

### Checking Error Codes

```
Process called create_file(path as Text) returns Boolean
    Let result = fopen(path.to_c_string(), "w".to_c_string())
    
    If result == Null
        Let error_code = get_last_error()
        Log.error("Failed to create file: " + error_code.to_text())
        Return False
    End If
    
    fclose(result)
    Return True
End Process
```

### Exception Handling

```
Process called process_data(path as Text) returns Any
    Try
        Let file_handle = open_file(path.to_c_string())
        If file_handle == Null
            Throw Exception("Failed to open file: " + path)
        End If
        
        # Process the file
        Let data = read_file_data(file_handle)
        close_file(file_handle)
        Return data
        
    Catch ex as Exception
        Log.error("Error processing file: " + ex.message)
        Return Null
    End Try
End Process
```

## Platform Considerations

### Platform Detection

```
Process called load_appropriate_library() returns Library
    If System.platform == "windows"
        Return Library.load("winlib.dll")
    Else If System.platform == "macos"
        Return Library.load("libmac.dylib")
    Else  # Linux/Unix
        Return Library.load("libunix.so")
    End If
End Process
```

### Architecture Specifics

```
Process called setup_memory() returns Boolean
    If System.architecture == "x86_64"
        Return initialize_64bit()
    Else If System.architecture == "arm64"
        Return initialize_arm64()
    Else
        Log.warning("Unsupported architecture: " + System.architecture)
        Return False
    End If
End Process
```

### Endianness

```
Process called read_binary_data(buffer as Pointer, size as Integer) returns Integer
    If System.is_little_endian
        Return read_le_value(buffer)
    Else
        Return read_be_value(buffer)
    End If
End Process
```

## Security Best Practices

### Restricting FFI Usage

Use sandboxing to limit FFI capabilities:

```
# In configuration
security.ffi.enabled = true
security.ffi.allowed_libraries = ["libc", "libmath"]
security.ffi.blocked_functions = ["system", "exec"]
```

### Input Validation

Always validate inputs before passing to native code:

```
Process called resize_image(path as Text, width as Integer, height as Integer) returns Boolean
    # Validate inputs
    If width <= 0 or height <= 0 or width > 10000 or height > 10000
        Log.error("Invalid dimensions for image resize")
        Return False
    End If
    
    If not File.exists(path)
        Log.error("Source file does not exist")
        Return False
    End If
    
    # Now safe to call native function
    Return image_library_resize(path.to_c_string(), width, height)
End Process
```

### Memory Safety

Avoid common memory-related vulnerabilities:

```
Process called get_user_name(id as Integer) returns Text
    # Allocate with proper bounds
    with Memory.allocate(256) as buffer
        # Zero the memory first
        Memory.zero(buffer, 256)
        
        # Call with proper size limits
        Let result = get_user_by_id(id, buffer, 255)  # Leave room for null terminator
        
        If result != 0
            Return Text.from_c_string(buffer)
        Else
            Return ""
        End If
    End with  # Automatic cleanup
End Process
```

## Performance Optimizations

### Reducing Marshalling Overhead

For performance-critical code:

```
Process called process_large_dataset(data as List of Decimal) returns Decimal
    # For large datasets, convert once instead of per-call
    Let data_ptr = data.to_c_array(Float64)
    Let result = 0.0
    
    # Make multiple native calls with the same data
    result = result + compute_sum(data_ptr, data.length())
    result = result + compute_average(data_ptr, data.length()) 
    result = result + compute_stddev(data_ptr, data.length())
    
    data_ptr.free()
    Return result
End Process
```

### Batch Processing

Process data in batches when possible:

```
Process called analyze_samples(samples as List of Integer) returns Map
    # Process in batches of 1000
    Let results = Map()
    Let batch_size = 1000
    
    For i from 0 to samples.length() step batch_size
        Let end = Math.min(i + batch_size, samples.length())
        Let batch = samples.slice(i, end)
        
        with batch.to_c_array(Int32) as batch_ptr
            Let batch_results = process_batch(batch_ptr, batch.length())
            results.merge(batch_results)
        End with
    End For
    
    Return results
End Process
```

## Examples

### Accessing File System (libc)

```
External Library "libc"

External Process called fopen(path as Pointer, mode as Pointer) returns Pointer from "libc"
External Process called fclose(handle as Pointer) returns Integer from "libc"
External Process called fread(buffer as Pointer, size as Integer, count as Integer, handle as Pointer) returns Integer from "libc"

Process called read_file_contents(path as Text) returns Text
    # Convert path to C string
    Let c_path = path.to_c_string()
    Let c_mode = "r".to_c_string()
    
    # Open the file
    Let file = fopen(c_path, c_mode)
    If file == Null
        Return ""
    End If
    
    # Read the contents
    with Memory.allocate(4096) as buffer
        Let bytes_read = fread(buffer, 1, 4096, file)
        Let content = Text.from_buffer(buffer, bytes_read)
        fclose(file)
        Return content
    End with
End Process
```

### Using a Graphics Library

```
External Library "graphics" with
    Windows = "graphics.dll",
    Linux = "libgraphics.so",
    MacOS = "libgraphics.dylib"
End

# Define structures for the graphics API
FFI Structure Color with
    r as Byte,
    g as Byte,
    b as Byte,
    a as Byte
End Structure

FFI Structure Point with
    x as Int32,
    y as Int32
End Structure

# Declare external functions
External Process called create_window(title as Pointer, width as Int32, height as Int32) returns Pointer from "graphics"
External Process called draw_line(window as Pointer, start as Pointer, end as Pointer, color as Pointer, thickness as Float32) returns Integer from "graphics"
External Process called destroy_window(window as Pointer) returns Void from "graphics"

# Create a simple drawing application
Process called create_drawing(title as Text, width as Integer, height as Integer) returns Boolean
    # Create the window
    Let c_title = title.to_c_string()
    Let window = create_window(c_title, width, height)
    
    If window == Null
        Log.error("Failed to create window")
        Return False
    End If
    
    # Create color and points
    Let red = Color()
    red.r = 255
    red.g = 0
    red.b = 0
    red.a = 255
    
    Let p1 = Point()
    p1.x = 10
    p1.y = 10
    
    Let p2 = Point()
    p2.x = width - 10
    p2.y = height - 10
    
    # Draw a diagonal line
    Let result = draw_line(window, p1.to_pointer(), p2.to_pointer(), red.to_pointer(), 2.0)
    
    # In a real app, you'd have an event loop here
    
    # Clean up
    destroy_window(window)
    Return True
End Process
```

### Database Access

```
External Library "sqlite3"

External Process called sqlite3_open(filename as Pointer, handle_ptr as Pointer) returns Integer from "sqlite3"
External Process called sqlite3_exec(handle as Pointer, sql as Pointer, callback as Pointer, callback_arg as Pointer, error_msg as Pointer) returns Integer from "sqlite3"
External Process called sqlite3_close(handle as Pointer) returns Integer from "sqlite3"
External Process called sqlite3_free(ptr as Pointer) returns Void from "sqlite3"

Process called callback_func(arg as Pointer, col_count as Integer, col_values as Pointer, col_names as Pointer) returns Integer
    # This would process each row returned from a query
    # For simplicity, we just log the first column value
    If col_count > 0 and col_values != Null
        Let value_ptr = Memory.read_pointer(col_values)
        If value_ptr != Null
            Let value = Text.from_c_string(value_ptr)
            Log.info("Database value: " + value)
        End If
    End If
    Return 0  # Continue processing
End Process

Process called query_database(db_path as Text, sql as Text) returns Boolean
    Let db_handle_ptr = Memory.allocate(8)  # Pointer to SQLite handle
    Let c_path = db_path.to_c_string()
    
    # Open database
    Let open_result = sqlite3_open(c_path, db_handle_ptr)
    If open_result != 0
        Log.error("Failed to open database")
        Memory.free(db_handle_ptr)
        Return False
    End If
    
    # Get the actual handle
    Let db_handle = Memory.read_pointer(db_handle_ptr)
    
    # Execute query
    Let c_sql = sql.to_c_string()
    Let error_msg_ptr = Memory.allocate(8)  # For error message pointer
    Let callback_ptr = FFI.create_callback(callback_func)
    
    Let exec_result = sqlite3_exec(db_handle, c_sql, callback_ptr, Null, error_msg_ptr)
    
    # Check for errors
    If exec_result != 0
        Let error_ptr = Memory.read_pointer(error_msg_ptr)
        If error_ptr != Null
            Let error_msg = Text.from_c_string(error_ptr)
            Log.error("SQL error: " + error_msg)
            sqlite3_free(error_ptr)
        End If
    End If
    
    # Clean up
    sqlite3_close(db_handle)
    Memory.free(db_handle_ptr)
    Memory.free(error_msg_ptr)
    callback_ptr.release()
    
    Return exec_result == 0
End Process
```

## References

- [RunaVM C API Reference](../API/RunaVM_C_API.md)
- [Memory Management Guide](../Memory/Management.md)
- [Security Best Practices](../Security/Sandboxing.md)
- [Native Library Integration](../Integration/Native_Libraries.md) 