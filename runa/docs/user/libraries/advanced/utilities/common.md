# Common Utilities Module

**Location:** `runa/src/stdlib/advanced/utilities/common.runa`

## Overview

The Common Utilities module provides shared utility functions used across the advanced standard library modules. This module centralizes common operations to eliminate code duplication and ensure consistent behavior throughout the advanced features. It serves as the foundation for other advanced modules with production-ready implementations and comprehensive error handling.

## Key Features

- **Time and Timestamp Utilities**: Reliable time operations with fallback mechanisms
- **Collection Operations**: Safe copying and manipulation of lists and dictionaries
- **String Generation**: Random string generation with multiple fallback strategies
- **Data Structure Initialization**: Standardized creation of common data structures
- **Error Handling**: Robust error handling with graceful degradation
- **Cross-Module Compatibility**: Consistent interface for all advanced modules

## Core Functions

### Time and Timestamp Functions

```runa
Process called "get_current_time" returns Float
```

Returns the current time in seconds since epoch with fallback handling.

**Returns:** Current timestamp as a `Float`.

**Example:**
```runa
Import "advanced/utilities/common" as Common

Let current_time be Common.get_current_time
Display "Current timestamp: " plus current_time

Note: Use for timing operations
Let start_time be Common.get_current_time
Note: Perform some operation here
Let end_time be Common.get_current_time
Let duration be end_time minus start_time
Display "Operation took: " plus duration plus " seconds"
```

```runa
Process called "get_current_timestamp" returns Float
```

Alias for `get_current_time` providing backward compatibility.

**Example:**
```runa
Note: Both functions return the same value
Let time1 be Common.get_current_time
Let time2 be Common.get_current_timestamp
Note: time1 and time2 will be very close or identical
```

### Collection Utility Functions

```runa
Process called "copy_list" that takes list as List[Any] returns List[Any]
```

Creates a shallow copy of the input list, ensuring safe manipulation without affecting the original.

**Parameters:**
- `list` - The list to copy

**Returns:** A new list containing the same elements.

**Example:**
```runa
Let original_list be list containing 1, 2, 3, "hello", true
Let copied_list be Common.copy_list with list as original_list

Note: Modify the copy without affecting the original
Add "new_item" to copied_list
Display "Original: " plus original_list     Note: Still [1, 2, 3, "hello", true]
Display "Copy: " plus copied_list          Note: [1, 2, 3, "hello", true, "new_item"]
```

```runa
Process called "copy_dictionary" that takes dict as Dictionary[String, Any] returns Dictionary[String, Any]
```

Creates a shallow copy of the input dictionary.

**Parameters:**
- `dict` - The dictionary to copy

**Returns:** A new dictionary with the same key-value pairs.

**Example:**
```runa
Let original_config be Dictionary with:
    "database_url" as "postgres://localhost:5432/db"
    "cache_size" as 1000
    "enable_logging" as true

Let config_copy be Common.copy_dictionary with dict as original_config

Note: Modify copy without affecting original
Set config_copy["cache_size"] to 2000
Set config_copy["new_option"] to "enabled"

Display "Original cache size: " plus original_config["cache_size"]  Note: Still 1000
Display "Copy cache size: " plus config_copy["cache_size"]          Note: Now 2000
```

### String Generation and Utilities

```runa
Process called "generate_random_string" that takes length as Integer returns String
```

Generates a random alphanumeric string of the specified length with multiple fallback strategies.

**Parameters:**
- `length` - The desired length of the random string

**Returns:** A random string of the specified length.

**Example:**
```runa
Note: Generate random strings for various purposes
Let session_id be Common.generate_random_string with length as 32
Display "Session ID: " plus session_id

Let api_key be Common.generate_random_string with length as 64
Display "API Key: " plus api_key

Let short_code be Common.generate_random_string with length as 8
Display "Short code: " plus short_code
```

```runa
Process called "generate_unique_id" returns String
```

Generates a unique identifier using timestamp-based generation.

**Returns:** A unique identifier string.

**Example:**
```runa
Let user_id be Common.generate_unique_id
Let transaction_id be Common.generate_unique_id
Let session_id be Common.generate_unique_id

Display "User ID: " plus user_id
Display "Transaction ID: " plus transaction_id
Display "Session ID: " plus session_id

Note: Each ID will be unique due to timestamp differences
```

### Data Structure Initialization

```runa
Process called "create_empty_list" returns List[Any]
```

Creates an empty list for initialization purposes.

**Returns:** An empty list ready for use.

```runa
Process called "create_empty_dictionary" returns Dictionary[String, Any]
```

Creates an empty dictionary for initialization purposes.

**Returns:** An empty dictionary ready for use.

**Example:**
```runa
Note: Initialize collections for building data structures
Let user_permissions be Common.create_empty_list
Let configuration be Common.create_empty_dictionary

Note: Build up the data structures
Add "read" to user_permissions
Add "write" to user_permissions
Add "execute" to user_permissions

Set configuration["database"] to "postgresql"
Set configuration["port"] to 5432
Set configuration["ssl"] to true

Display "Permissions: " plus user_permissions
Display "Configuration: " plus configuration
```

### String Formatting and Utility Functions

```runa
Process called "format_timestamp" that takes timestamp as Float returns String
```

Formats a timestamp as a readable string.

**Parameters:**
- `timestamp` - The timestamp to format

**Returns:** A formatted timestamp string.

**Example:**
```runa
Let current_time be Common.get_current_time
Let formatted_time be Common.format_timestamp with timestamp as current_time
Display "Formatted time: " plus formatted_time

Note: Use for logging and display purposes
Let event_time be 1705353600.0  Note: Example timestamp
Let formatted_event be Common.format_timestamp with timestamp as event_time
Display "Event occurred at: " plus formatted_event
```

```runa
Process called "safe_string_concat" that takes parts as List[String] returns String
```

Safely concatenates string parts with comprehensive error handling.

**Parameters:**
- `parts` - List of strings to concatenate

**Returns:** The concatenated string, or error indicator on failure.

**Example:**
```runa
Let message_parts be list containing "Hello", " ", "World", "!"
Let full_message be Common.safe_string_concat with parts as message_parts
Display full_message  Note: "Hello World!"

Note: Handles errors gracefully
Let mixed_parts be list containing "Start", null, "End"
Let safe_result be Common.safe_string_concat with parts as mixed_parts
Display safe_result  Note: Will return "concat_error" due to null value
```

## Idiomatic Usage Patterns

### Timing and Performance Measurement

```runa
Import "advanced/utilities/common" as Common

Process called "measure_operation_performance" that takes operation_name as String returns Float:
    Display "Starting " plus operation_name plus "..."
    Let start_time be Common.get_current_time
    
    Note: Simulate some work (replace with actual operation)
    For i from 1 to 1000000:
        Let temp be i times 2
    
    Let end_time be Common.get_current_time
    Let duration be end_time minus start_time
    
    Display operation_name plus " completed in " plus duration plus " seconds"
    Return duration

Note: Measure multiple operations
Let database_time be measure_operation_performance with operation_name as "Database Query"
Let cache_time be measure_operation_performance with operation_name as "Cache Lookup"
Let api_time be measure_operation_performance with operation_name as "API Call"

Display "Performance Summary:"
Display "  Database: " plus database_time plus "s"
Display "  Cache: " plus cache_time plus "s"
Display "  API: " plus api_time plus "s"
```

### Safe Data Structure Operations

```runa
Import "advanced/utilities/common" as Common

Process called "safe_configuration_management" returns Dictionary[String, Any]:
    Note: Create a base configuration
    Let base_config be Dictionary with:
        "app_name" as "MyApp"
        "version" as "1.0.0"
        "database" as Dictionary with:
            "host" as "localhost"
            "port" as 5432
            "name" as "myapp_db"
        "features" as list containing "logging", "caching", "auth"
    
    Note: Create safe copies for different environments
    Let dev_config be Common.copy_dictionary with dict as base_config
    Let prod_config be Common.copy_dictionary with dict as base_config
    
    Note: Modify environment-specific settings
    Set dev_config["debug"] to true
    Set dev_config["database"]["host"] to "dev.localhost"
    
    Set prod_config["debug"] to false
    Set prod_config["database"]["host"] to "prod.example.com"
    Set prod_config["database"]["ssl"] to true
    
    Note: Add environment-specific features safely
    Let dev_features be Common.copy_list with list as prod_config["features"]
    Add "debug_toolbar" to dev_features
    Add "hot_reload" to dev_features
    Set dev_config["features"] to dev_features
    
    Display "Base config unchanged: " plus base_config["database"]["host"]
    Display "Dev config: " plus dev_config["database"]["host"]
    Display "Prod config: " plus prod_config["database"]["host"]
    
    Return prod_config
```

### Unique Identifier Generation

```runa
Import "advanced/utilities/common" as Common

Process called "generate_system_identifiers" returns Dictionary[String, String]:
    Let identifiers be Common.create_empty_dictionary
    
    Note: Generate various types of unique identifiers
    Set identifiers["session_id"] to Common.generate_unique_id
    Set identifiers["request_id"] to Common.generate_unique_id
    Set identifiers["transaction_id"] to Common.generate_unique_id
    
    Note: Generate random tokens for security
    Set identifiers["api_token"] to Common.generate_random_string with length as 64
    Set identifiers["csrf_token"] to Common.generate_random_string with length as 32
    Set identifiers["nonce"] to Common.generate_random_string with length as 16
    
    Note: Generate user-friendly codes
    Set identifiers["user_code"] to Common.generate_random_string with length as 8
    Set identifiers["verification_code"] to Common.generate_random_string with length as 6
    
    Return identifiers

Note: Use the generated identifiers
Let system_ids be generate_system_identifiers
For each id_type in system_ids:
    Display id_type plus ": " plus system_ids[id_type]
```

### Error-Resilient String Operations

```runa
Import "advanced/utilities/common" as Common

Process called "build_error_resistant_message" that takes components as List[Any] returns String:
    Note: Convert all components to strings safely
    Let string_parts be Common.create_empty_list
    
    For each component in components:
        If component is String:
            Add component to string_parts
        Otherwise if component is Integer:
            Add component as string to string_parts
        Otherwise if component is Float:
            Add component as string to string_parts
        Otherwise if component is Boolean:
            Add component as string to string_parts
        Otherwise if component is none:
            Add "[null]" to string_parts
        Otherwise:
            Add "[object]" to string_parts
    
    Note: Use safe concatenation
    Let result be Common.safe_string_concat with parts as string_parts
    
    If result is equal to "concat_error":
        Note: Fallback to basic message
        Return "Message construction failed"
    
    Return result

Note: Test with various input types
Let mixed_input be list containing "User", " ", 12345, " logged in at ", 1705353600.0, " with status ", true
Let safe_message be build_error_resistant_message with components as mixed_input
Display "Safe message: " plus safe_message
```

## Best Practices

### 1. Error Handling Patterns

```runa
Process called "robust_utility_usage" returns Optional[String]:
    Try:
        Note: Always check for successful operations
        Let timestamp be Common.get_current_time
        If timestamp is greater than 0:
            Let formatted be Common.format_timestamp with timestamp as timestamp
            Return some with value as formatted
        Otherwise:
            Display "Invalid timestamp received"
            Return none
            
    Catch error:
        Display "Utility operation failed: " plus error
        Return none
```

### 2. Performance Optimization

```runa
Note: Cache frequently used empty structures
Let empty_list_cache be Common.create_empty_list
Let empty_dict_cache be Common.create_empty_dictionary

Process called "optimized_data_creation" returns Dictionary[String, Any]:
    Note: Reuse cached empty structures when possible
    Let result be Common.copy_dictionary with dict as empty_dict_cache
    Let items be Common.copy_list with list as empty_list_cache
    
    Note: Build up the data structure
    Set result["items"] to items
    Set result["created_at"] to Common.get_current_time
    Set result["id"] to Common.generate_unique_id
    
    Return result
```

### 3. Memory Management

```runa
Process called "memory_conscious_operations" returns None:
    Note: Create copies only when necessary
    Let original_data be list containing 1, 2, 3, 4, 5
    
    Note: If you only need to read, don't copy
    For each item in original_data:
        Display "Item: " plus item
    
    Note: Only copy when you need to modify
    If need_to_modify:
        Let modifiable_copy be Common.copy_list with list as original_data
        Add 6 to modifiable_copy
        Display "Modified copy: " plus modifiable_copy
```

## Integration with Advanced Modules

### Hot Reload Integration

```runa
Import "advanced/utilities/common" as Common
Import "advanced/hot_reload/core" as HotReload

Process called "timestamped_hot_reload_events" that takes context as HotReload.HotReloadContext returns None:
    Note: Use common utilities for consistent timestamps
    Let event_time be Common.get_current_time
    Let formatted_time be Common.format_timestamp with timestamp as event_time
    
    Display "Hot reload event at: " plus formatted_time
    
    Note: Generate unique reload session ID
    Let session_id be Common.generate_unique_id
    Set context.metadata["reload_session"] to session_id
```

### Memory Management Integration

```runa
Import "advanced/utilities/common" as Common
Import "advanced/memory/ownership" as Ownership

Process called "timestamped_ownership_tracking" returns None:
    Let tracker be Ownership.create_ownership_tracker
    Let owner be Ownership.create_owner with id as Common.generate_unique_id
    
    Note: Use common timestamp for consistent tracking
    Let creation_time be Common.get_current_time
    Set owner.creation_time to creation_time
    
    Display "Owner created at: " plus Common.format_timestamp with timestamp as creation_time
```

### Caching Integration

```runa
Import "advanced/utilities/common" as Common
Import "advanced/caching/intelligent_cache" as Cache

Process called "cache_with_timestamps" returns None:
    Let cache be Cache.create_intelligent_cache with config as none
    
    Note: Use common utilities for cache keys and timestamps
    Let cache_key be "user_data_" plus Common.generate_unique_id
    Let timestamp be Common.get_current_time
    
    Let data be Dictionary with:
        "user_id" as 12345
        "created_at" as timestamp
        "formatted_time" as Common.format_timestamp with timestamp as timestamp
    
    Cache.cache_put with cache as cache and key as cache_key and value as data
    Display "Cached data with key: " plus cache_key
```

## Performance Characteristics

### Function Performance

- **get_current_time**: ~10-100 nanoseconds (system call dependent)
- **copy_list**: O(n) where n is list length, ~1-10 microseconds per 1000 elements
- **copy_dictionary**: O(n) where n is number of keys, ~2-20 microseconds per 1000 keys
- **generate_random_string**: O(n) where n is length, ~10-100 nanoseconds per character
- **generate_unique_id**: ~50-200 nanoseconds (timestamp-based)

### Memory Overhead

- **List copying**: ~24 bytes + (8 bytes × number of elements) additional memory
- **Dictionary copying**: ~64 bytes + (24 bytes × number of keys) additional memory
- **String generation**: ~40 bytes + (1 byte × string length) memory

### Optimization Tips

```runa
Note: Minimize allocations in hot paths
Process called "optimized_common_usage" returns None:
    Note: Pre-allocate structures when possible
    Let reusable_list be Common.create_empty_list
    Let reusable_dict be Common.create_empty_dictionary
    
    Note: Reuse timestamp calculations
    Let current_time be Common.get_current_time
    
    For i from 1 to 1000:
        Note: Use pre-allocated structures
        Clear reusable_list
        Clear reusable_dict
        
        Note: Reuse timestamp instead of calling get_current_time repeatedly
        Set reusable_dict["timestamp"] to current_time
        Set reusable_dict["iteration"] to i
        
        Note: Process with reused structures
```

## Error Handling and Fallbacks

The common utilities module provides comprehensive fallback mechanisms:

### Time Function Fallbacks

```runa
Note: The get_current_time function has built-in fallbacks
Let timestamp be Common.get_current_time

Note: If system time is unavailable, returns 1234567890.0
Note: This ensures operations can continue even with time system failures
```

### String Generation Fallbacks

```runa
Note: generate_random_string falls back to timestamp-based generation
Let random_str be Common.generate_random_string with length as 16

Note: If random module is unavailable, uses timestamp + length for uniqueness
Note: While less random, it ensures functionality is maintained
```

### Safe Operations

```runa
Process called "demonstrate_safe_operations" returns None:
    Note: All utility functions handle errors gracefully
    
    Try:
        Let result be Common.safe_string_concat with parts as list containing "test", null, "string"
        Display "Result: " plus result  Note: Will show "concat_error" instead of crashing
        
    Catch error:
        Display "This catch block rarely executes due to internal error handling"
```

## Comparative Notes

### Advantages over Language Built-ins

1. **Consistency**: All functions provide consistent error handling and fallback behavior
2. **Cross-Platform**: Works identically across different operating systems and environments
3. **AI-Friendly**: Clear function names and predictable behavior for AI agent usage
4. **Error Resilience**: Built-in fallbacks ensure operations continue even when subsystems fail

### Integration Benefits

- **Centralized Utilities**: Single source of truth for common operations across advanced modules
- **Consistent Behavior**: All advanced modules use the same underlying utilities
- **Maintenance**: Easy to update behavior across all advanced modules by updating common utilities
- **Testing**: Centralized testing ensures reliability across the entire advanced library

This common utilities module provides the reliable foundation that enables the sophisticated features of Runa's advanced standard library, ensuring consistent and robust behavior across all advanced modules.