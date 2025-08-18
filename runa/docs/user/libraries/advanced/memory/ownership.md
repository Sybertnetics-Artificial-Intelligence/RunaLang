# Memory Ownership Module

**Location:** `runa/src/stdlib/advanced/memory/ownership.runa`

## Overview

The Memory Ownership module provides a comprehensive ownership and borrowing system for memory safety, inspired by Rust but adapted for Runa's natural language syntax and AI-first design principles. This production-ready system ensures memory safety through compile-time and runtime checks while maintaining ergonomic usability for both humans and AI agents.

## Key Features

- **Ownership Tracking**: Complete ownership management for memory pointers and references
- **Borrowing System**: Safe borrowing with mutable and immutable reference types
- **Lifetime Management**: Automatic scope tracking and cleanup mechanisms
- **Memory Safety**: Prevention of use-after-free, double-free, and memory leak errors
- **AI-First Design**: Natural language syntax optimized for AI agent comprehension
- **Production Ready**: Comprehensive validation, thread safety, and error handling
- **Integration Ready**: Seamless integration with allocators and garbage collector

## Types and Interfaces

### Core Ownership Types

```runa
Type called "Owner":
    id as String
    owned_pointers as List[Pointer]
    creation_time as Float
    active as Boolean
    metadata as Dictionary[String, Any]

Type called "Pointer":
    address as Integer
    size as Integer
    type_info as String
    metadata as Dictionary[String, Any]

Type called "BorrowHandle":
    pointer as Pointer
    borrow_type as BorrowType
    owner as Owner
    scope_id as String
    creation_time as Float
    active as Boolean
    metadata as Dictionary[String, Any]

Type BorrowType is:
    | Mutable
    | Immutable
```

### Tracking and Management

```runa
Type called "OwnershipTracker":
    owners as Dictionary[String, Owner]
    borrowed_pointers as Dictionary[Pointer, BorrowInfo]
    lifetime_scopes as List[LifetimeScope]
    current_scope_id as String
    error_log as List[String]
    performance_metrics as Dictionary[String, Float]
    metadata as Dictionary[String, Any]

Type called "BorrowInfo":
    borrow_type as BorrowType
    active as Boolean
    creation_time as Float
    scope_id as String
    metadata as Dictionary[String, Any]

Type called "LifetimeScope":
    id as String
    active as Boolean
    pointers as List[Pointer]
    parent_scope as Optional[String]
    creation_time as Float
    metadata as Dictionary[String, Any]
```

## Core Functions

### Ownership Management

```runa
Process called "create_ownership_tracker" returns OwnershipTracker
```

Creates a new ownership tracker for managing memory ownership across your application.

**Returns:** A fresh `OwnershipTracker` with empty state.

**Example:**
```runa
Import "advanced/memory/ownership" as Ownership

Let tracker be Ownership.create_ownership_tracker
Display "Ownership tracker created and ready"
```

```runa
Process called "create_owner" that takes id as String returns Owner
```

Creates a new owner that can own memory pointers.

**Parameters:**
- `id` - Unique identifier for the owner

**Returns:** New `Owner` instance ready to own pointers.

**Example:**
```runa
Let main_owner be Ownership.create_owner with id as "main_application"
Let buffer_owner be Ownership.create_owner with id as "image_buffer_manager"
```

```runa
Process called "add_ownership" that takes tracker as OwnershipTracker and owner as Owner and pointer as Pointer returns Boolean
```

Assigns ownership of a pointer to an owner, ensuring no double ownership.

**Example:**
```runa
Let pointer be Ownership.create_pointer with address as 0x1000 and size as 1024 and type_info as "ByteBuffer"
Let success be Ownership.add_ownership with tracker as tracker and owner as main_owner and pointer as pointer

If success:
    Display "Ownership established successfully"
Otherwise:
    Let errors be tracker.error_log
    Display "Ownership failed: " plus errors[errors size minus 1]
```

### Borrowing System

```runa
Process called "create_borrow" that takes tracker as OwnershipTracker and owner as Owner and pointer as Pointer and borrow_type as BorrowType returns Optional[BorrowHandle]
```

Creates a borrow of a pointer, ensuring borrowing rules are respected.

**Parameters:**
- `tracker` - The ownership tracker
- `owner` - The owner of the pointer
- `pointer` - The pointer to borrow
- `borrow_type` - Either `Mutable` or `Immutable`

**Returns:** `BorrowHandle` if successful, `none` if borrowing rules violated.

**Example:**
```runa
Note: Create an immutable borrow for reading
Let read_borrow be Ownership.create_borrow with tracker as tracker and owner as main_owner and pointer as pointer and borrow_type as Immutable

Match read_borrow:
    When some with value as handle:
        Display "Created immutable borrow successfully"
        Note: Use the borrowed data here
        Let ended be Ownership.end_borrow with tracker as tracker and handle as handle
    When none:
        Display "Could not create borrow - check ownership and existing borrows"

Note: Create a mutable borrow for writing (only one allowed at a time)
Let write_borrow be Ownership.create_borrow with tracker as tracker and owner as main_owner and pointer as pointer and borrow_type as Mutable

Match write_borrow:
    When some with value as handle:
        Display "Created mutable borrow successfully"
        Note: Modify the data here
        Let ended be Ownership.end_borrow with tracker as tracker and handle as handle
    When none:
        Display "Could not create mutable borrow - likely already borrowed"
```

### Lifetime Management

```runa
Process called "create_lifetime_scope" that takes tracker as OwnershipTracker and scope_id as String and parent_scope as Optional[String] returns LifetimeScope
```

Creates a new lifetime scope for managing pointer lifetimes.

**Example:**
```runa
Note: Create nested scopes for different contexts
Let main_scope be Ownership.create_lifetime_scope with tracker as tracker and scope_id as "main" and parent_scope as none
Let function_scope be Ownership.create_lifetime_scope with tracker as tracker and scope_id as "function_context" and parent_scope as some with value as "main"

Note: Enter and exit scopes as needed
Ownership.enter_lifetime_scope with tracker as tracker and scope as function_scope

Note: Your code using pointers in this scope
Note: ...

Ownership.exit_lifetime_scope with tracker as tracker and scope_id as "function_context"
```

## Idiomatic Usage Patterns

### Basic Memory Management

```runa
Import "advanced/memory/ownership" as Ownership

Process called "basic_memory_management_example" returns None:
    Note: Set up ownership tracking
    Let tracker be Ownership.create_ownership_tracker
    Let owner be Ownership.create_owner with id as "main"
    
    Note: Allocate and own some memory
    Let data_pointer be Ownership.create_pointer with address as 0x2000 and size as 2048 and type_info as "UserData"
    Let owned be Ownership.add_ownership with tracker as tracker and owner as owner and pointer as data_pointer
    
    If owned:
        Note: Create a read-only borrow
        Let read_handle be Ownership.create_borrow with tracker as tracker and owner as owner and pointer as data_pointer and borrow_type as Immutable
        
        Match read_handle:
            When some with value as handle:
                Note: Safe to read from the pointer
                Display "Reading data safely through borrow"
                
                Note: End the borrow when done
                Ownership.end_borrow with tracker as tracker and handle as handle
                
                Note: Now we can create a mutable borrow
                Let write_handle be Ownership.create_borrow with tracker as tracker and owner as owner and pointer as data_pointer and borrow_type as Mutable
                
                Match write_handle:
                    When some with value as write_h:
                        Display "Writing data safely through mutable borrow"
                        Ownership.end_borrow with tracker as tracker and handle as write_h
                    When none:
                        Display "Could not create mutable borrow"
                        
            When none:
                Display "Could not create initial borrow"
    Otherwise:
        Display "Failed to establish ownership"
```

### Safe Resource Management

```runa
Import "advanced/memory/ownership" as Ownership

Process called "safe_resource_manager" returns None:
    Let tracker be Ownership.create_ownership_tracker
    
    Note: Create different owners for different subsystems
    Let network_owner be Ownership.create_owner with id as "network_subsystem"
    Let cache_owner be Ownership.create_owner with id as "cache_subsystem"
    
    Note: Allocate resources for each subsystem
    Let network_buffer be Ownership.create_pointer with address as 0x3000 and size as 4096 and type_info as "NetworkBuffer"
    Let cache_buffer be Ownership.create_pointer with address as 0x4000 and size as 8192 and type_info as "CacheBuffer"
    
    Ownership.add_ownership with tracker as tracker and owner as network_owner and pointer as network_buffer
    Ownership.add_ownership with tracker as tracker and owner as cache_owner and pointer as cache_buffer
    
    Note: Transfer ownership if needed
    Let transferred be Ownership.transfer_ownership with tracker as tracker and from_owner as network_owner and to_owner as cache_owner and pointer as network_buffer
    
    If transferred:
        Display "Successfully transferred network buffer to cache subsystem"
        
        Note: Validate the ownership state
        Let valid be Ownership.validate_ownership_state with tracker as tracker
        If valid:
            Display "All ownership invariants maintained"
        Otherwise:
            Display "Warning: Ownership validation failed"
            For each error in tracker.error_log:
                Display "Validation error: " plus error
    
    Note: Get statistics about ownership
    Let stats be Ownership.get_ownership_statistics with tracker as tracker
    Display "Total owners: " plus stats["total_owners"]
    Display "Total pointers: " plus stats["total_pointers"]
    Display "Active borrows: " plus stats["active_borrows"]
```

### Advanced Scope Management

```runa
Import "advanced/memory/ownership" as Ownership

Process called "advanced_scope_example" returns None:
    Let tracker be Ownership.create_ownership_tracker
    Let owner be Ownership.create_owner with id as "scope_demo"
    
    Note: Create hierarchical scopes
    Let main_scope be Ownership.create_lifetime_scope with tracker as tracker and scope_id as "main" and parent_scope as none
    Ownership.enter_lifetime_scope with tracker as tracker and scope as main_scope
    
    Note: Allocate memory in main scope
    Let main_data be Ownership.create_pointer with address as 0x5000 and size as 1024 and type_info as "MainData"
    Ownership.add_ownership with tracker as tracker and owner as owner and pointer as main_data
    
    Note: Enter a nested scope
    Let nested_scope be Ownership.create_lifetime_scope with tracker as tracker and scope_id as "nested" and parent_scope as some with value as "main"
    Ownership.enter_lifetime_scope with tracker as tracker and scope as nested_scope
    
    Note: Create borrow in nested scope
    Let nested_borrow be Ownership.create_borrow with tracker as tracker and owner as owner and pointer as main_data and borrow_type as Immutable
    
    Match nested_borrow:
        When some with value as handle:
            Display "Created borrow in nested scope"
            
            Note: Exit nested scope (automatically ends borrows)
            Ownership.exit_lifetime_scope with tracker as tracker and scope_id as "nested"
            Display "Exited nested scope - borrows automatically cleaned up"
            
        When none:
            Display "Could not create borrow in nested scope"
    
    Note: Exit main scope
    Ownership.exit_lifetime_scope with tracker as tracker and scope_id as "main"
    Display "Exited main scope"
    
    Note: Clean up inactive borrows
    Let cleaned_count be Ownership.cleanup_inactive_borrows with tracker as tracker
    Display "Cleaned up " plus cleaned_count plus " inactive borrows"
```

## Best Practices

### 1. Ownership Design Patterns

**Single Owner Pattern:**
```runa
Note: One clear owner for each resource
Let buffer_owner be Ownership.create_owner with id as "image_processor"
Let image_buffer be Ownership.create_pointer with address as buffer_address and size as image_size and type_info as "ImageData"
Ownership.add_ownership with tracker as tracker and owner as buffer_owner and pointer as image_buffer
```

**Temporary Transfer Pattern:**
```runa
Note: Temporarily transfer ownership for processing
Let processing_owner be Ownership.create_owner with id as "image_filter"
Let transferred be Ownership.transfer_ownership with tracker as tracker and from_owner as buffer_owner and to_owner as processing_owner and pointer as image_buffer

Note: Process the image...

Note: Transfer back when done
Ownership.transfer_ownership with tracker as tracker and from_owner as processing_owner and to_owner as buffer_owner and pointer as image_buffer
```

### 2. Safe Borrowing Patterns

**Read-Many Pattern:**
```runa
Note: Multiple immutable borrows are allowed
Let reader1 be Ownership.create_borrow with tracker as tracker and owner as owner and pointer as data and borrow_type as Immutable
Let reader2 be Ownership.create_borrow with tracker as tracker and owner as owner and pointer as data and borrow_type as Immutable
Let reader3 be Ownership.create_borrow with tracker as tracker and owner as owner and pointer as data and borrow_type as Immutable

Note: All can read simultaneously
Note: End all borrows when done
```

**Write-Exclusive Pattern:**
```runa
Note: Only one mutable borrow allowed
Let writer be Ownership.create_borrow with tracker as tracker and owner as owner and pointer as data and borrow_type as Mutable

Match writer:
    When some with value as handle:
        Note: Exclusive access for writing
        Note: No other borrows can exist
        Ownership.end_borrow with tracker as tracker and handle as handle
    When none:
        Display "Cannot write - resource is borrowed"
```

### 3. Error Handling and Validation

```runa
Process called "robust_ownership_management" that takes tracker as OwnershipTracker returns Boolean:
    Try:
        Note: Regularly validate ownership state
        Let valid be Ownership.validate_ownership_state with tracker as tracker
        If not valid:
            Display "Ownership validation failed!"
            For each error in tracker.error_log:
                Display "Error: " plus error
            Return false
        
        Note: Check for memory leaks
        Let stats be Ownership.get_ownership_statistics with tracker as tracker
        If stats["active_borrows"] is greater than 100:
            Display "Warning: High number of active borrows (" plus stats["active_borrows"] plus ")"
            
        If stats["total_pointers"] is greater than 1000:
            Display "Warning: High number of tracked pointers (" plus stats["total_pointers"] plus ")"
        
        Return true
        
    Catch error:
        Display "Ownership management error: " plus error
        Return false
```

## Performance Considerations

### Memory Overhead

The ownership system adds minimal overhead:
- **Owner**: ~64 bytes per owner
- **Pointer Tracking**: ~48 bytes per tracked pointer
- **Borrow Handle**: ~56 bytes per active borrow
- **Scope Tracking**: ~40 bytes per lifetime scope

### Optimization Strategies

```runa
Note: Optimize ownership tracking performance
Process called "optimize_ownership_tracking" that takes tracker as OwnershipTracker returns None:
    Note: Clean up inactive borrows regularly
    Let cleaned be Ownership.cleanup_inactive_borrows with tracker as tracker
    If cleaned is greater than 0:
        Display "Cleaned up " plus cleaned plus " inactive borrows"
    
    Note: Validate ownership state periodically, not on every operation
    Let stats be Ownership.get_ownership_statistics with tracker as tracker
    If stats["total_operations"] modulo 1000 is equal to 0:
        Let valid be Ownership.validate_ownership_state with tracker as tracker
        If not valid:
            Display "Ownership validation failed - check for issues"
```

### Benchmarking

```runa
Process called "benchmark_ownership_system" returns Dictionary[String, Float]:
    Let tracker be Ownership.create_ownership_tracker
    Let owner be Ownership.create_owner with id as "benchmark"
    Let start_time be get_current_time
    
    Note: Benchmark ownership operations
    For i from 1 to 1000:
        Let pointer be Ownership.create_pointer with address as i and size as 1024 and type_info as "BenchmarkData"
        Ownership.add_ownership with tracker as tracker and owner as owner and pointer as pointer
    
    Let ownership_time be get_current_time minus start_time
    Let borrow_start_time be get_current_time
    
    Note: Benchmark borrowing operations
    For i from 1 to 1000:
        Let pointer be Ownership.create_pointer with address as i and size as 1024 and type_info as "BenchmarkData"
        Let borrow be Ownership.create_borrow with tracker as tracker and owner as owner and pointer as pointer and borrow_type as Immutable
        Match borrow:
            When some with value as handle:
                Ownership.end_borrow with tracker as tracker and handle as handle
            When none:
                Note: Expected for non-owned pointers
                Pass
    
    Let borrow_time be get_current_time minus borrow_start_time
    
    Return Dictionary with:
        "ownership_ops_per_second" as 1000 divided by ownership_time
        "borrow_ops_per_second" as 1000 divided by borrow_time
        "memory_overhead_bytes" as tracker.owners size times 64 plus tracker.borrowed_pointers size times 48
```

## Integration with Other Memory Modules

### Garbage Collector Integration

```runa
Import "advanced/memory/gc" as GC

Process called "integrate_with_gc" that takes tracker as OwnershipTracker returns None:
    Note: Provide ownership information to GC for optimization
    Let gc_context be GC.create_gc_context
    
    Let stats be Ownership.get_ownership_statistics with tracker as tracker
    GC.set_ownership_hints with context as gc_context and owned_pointers as stats["total_pointers"] and active_borrows as stats["active_borrows"]
    
    Note: GC can avoid collecting owned pointers
    For each owner_id in tracker.owners:
        Let owner be tracker.owners[owner_id]
        For each pointer in owner.owned_pointers:
            GC.mark_pointer_as_owned with context as gc_context and pointer as pointer
```

### Memory Allocator Integration

```runa
Import "advanced/memory/custom_allocators" as Allocators

Process called "integrate_with_allocator" that takes tracker as OwnershipTracker returns None:
    Let allocator be Allocators.create_tracking_allocator
    
    Note: Hook allocator to automatically register ownership
    Process called "allocation_hook" that takes pointer as Pointer and owner_id as String returns None:
        Let owner be Ownership.create_owner with id as owner_id
        Ownership.add_ownership with tracker as tracker and owner as owner and pointer as pointer
    
    Allocators.set_allocation_callback with allocator as allocator and callback as allocation_hook
```

## Comparative Notes

### Advantages over Traditional Memory Management

1. **C/C++ vs Runa**: Eliminates manual memory management and use-after-free bugs automatically
2. **Rust vs Runa**: More natural syntax while maintaining similar safety guarantees
3. **Java/C# vs Runa**: Provides explicit ownership control while maintaining memory safety
4. **Python vs Runa**: Eliminates reference cycles and provides deterministic cleanup

### AI-First Design Benefits

- **Natural Language Syntax**: Easy for AI agents to understand and generate
- **Explicit Ownership**: Clear ownership semantics for AI reasoning
- **Comprehensive Validation**: Built-in checking helps AI agents avoid errors
- **Error Recovery**: Detailed error messages assist AI in debugging

## Error Handling and Recovery

The ownership system provides detailed error reporting and recovery mechanisms:

```runa
Process called "handle_ownership_errors" that takes tracker as OwnershipTracker returns None:
    For each error in tracker.error_log:
        If "double ownership" in error:
            Display "🚨 Double ownership detected - this indicates a serious bug"
            Note: Investigate immediately
        
        If "invalid borrow" in error:
            Display "⚠️ Invalid borrow attempt - check borrow rules"
            Note: Ensure no conflicting borrows exist
        
        If "use after free" in error:
            Display "💥 Use after free detected - memory safety violation"
            Note: Check pointer lifetimes and scope management
        
        If "memory leak" in error:
            Display "🔍 Potential memory leak - check cleanup"
            Note: Ensure all owned pointers are properly released
```

This memory ownership module provides the foundation for safe, efficient memory management in Runa applications, essential for building reliable AI-first systems.