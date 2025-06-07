# Runa Virtual Machine (RunaVM)

The Runa Virtual Machine (RunaVM) is the core runtime system that executes Runa bytecode, providing a consistent execution environment across platforms. This document covers the architecture, features, and usage of RunaVM.

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [VM Features](#vm-features)
4. [Memory Management](#memory-management)
5. [Concurrency Model](#concurrency-model)
6. [Interoperability](#interoperability)
7. [Performance Optimization](#performance-optimization)
8. [Security Features](#security-features)
9. [Deployment Options](#deployment-options)
10. [Troubleshooting](#troubleshooting)
11. [References](#references)

## Overview

RunaVM is designed to efficiently execute Runa bytecode, offering a balance between performance and portability. It serves as the foundation for running Runa applications on any supported platform without recompilation.

### Key Advantages

- **Consistent Cross-Platform Execution**: Unified behavior across operating systems
- **Performance**: Optimized execution with JIT compilation where available
- **Memory Safety**: Automatic memory management and boundary checks
- **Secure Execution**: Sandboxed environment with configurable security policies
- **Interoperability**: Seamless integration with host platforms and native libraries

### Native vs. VM Execution

While Runa can be transpiled to target languages (Python, JavaScript, etc.), using RunaVM offers several benefits:

- **Consistent Behavior**: Identical execution across all platforms
- **Simplified Deployment**: Single runtime for all systems
- **Enhanced Security**: Sandboxed execution environment
- **Advanced Features**: Access to RunaVM-specific optimizations and capabilities
- **Direct Access**: First-class support for all Runa language features

### Supported Platforms

RunaVM is available on:

- **Windows**: 10 and newer (x86_64, ARM64)
- **macOS**: 10.15+ (x86_64, Apple Silicon)
- **Linux**: Most modern distributions (x86_64, ARM64, ARM32)
- **Web Browsers**: Via WebAssembly
- **Mobile**: iOS 13+, Android 8.0+
- **Embedded Systems**: Select platforms with 32MB+ RAM

## Architecture

### Component Overview

The RunaVM architecture consists of:

```
┌───────────────────────────────────────┐
│              User Code                │
└───────────────────────────────────────┘
               ↓
┌───────────────────────────────────────┐
│          Bytecode Loader              │
└───────────────────────────────────────┘
               ↓
┌───────────────────────────────────────┐
│          Execution Engine             │
├───────────┬───────────────┬───────────┤
│ Interpreter│  JIT Compiler │ Optimizer │
└───────────┴───────────────┴───────────┘
               ↓
┌───────────────────────────────────────┐
│          Runtime Systems              │
├───────────┬───────────────┬───────────┤
│  Memory   │  Concurrency  │ Exception │
│ Management│    Model      │ Handling  │
└───────────┴───────────────┴───────────┘
               ↓
┌───────────────────────────────────────┐
│       Platform Integration Layer      │
└───────────────────────────────────────┘
               ↓
┌───────────────────────────────────────┐
│         Host Operating System         │
└───────────────────────────────────────┘
```

### Bytecode Format

RunaVM executes a compact, efficient bytecode format:

- **Instruction Set**: RISC-inspired design with ~120 core instructions
- **Type System**: Rich type information preserved in bytecode
- **Metadata**: Debugging information, optimizations hints, security annotations
- **Format Version**: Current bytecode version: 1.2

To inspect bytecode:

```bash
runavm --disassemble my_program.runab
```

### Execution Model

RunaVM uses a hybrid execution approach:

1. **Interpretation**: Initial execution via bytecode interpreter
2. **Profiling**: Runtime analysis of hot code paths
3. **JIT Compilation**: Dynamic compilation of frequently executed code
4. **Optimization**: Continuous performance improvements during execution

## VM Features

### Type System

The VM implements Runa's rich type system:

- **Primitive Types**: Integer, Decimal, Boolean, Text, etc.
- **Compound Types**: Lists, Maps, Tuples, Structures
- **Function Types**: First-class function values with closure support
- **Optional Types**: Explicit handling of nullable values
- **Type Checking**: Runtime type verification

### Standard Library

RunaVM includes a comprehensive standard library:

- **Core**: Basic programming constructs and data structures
- **Math**: Mathematical operations and algorithms
- **IO**: File system, networking, and data streams
- **Text**: String manipulation and pattern matching
- **Collections**: Advanced data structure operations
- **Concurrency**: Parallel processing primitives
- **Time**: Date, time, and duration utilities
- **System**: Operating system interface
- **Crypto**: Cryptographic algorithms and security utilities

### Error Handling

Robust exception mechanism:

- **Structured Exceptions**: Hierarchical exception types
- **Detailed Information**: Stack traces with source location
- **Resource Cleanup**: Automatic handling via finally blocks
- **Error Recovery**: Resumable exceptions where appropriate

### Introspection and Reflection

Runtime system examination:

- **Type Inspection**: Examine type information at runtime
- **Function Reflection**: Inspect function signatures and metadata
- **Dynamic Invocation**: Call functions by name or reference
- **Memory Analysis**: Examine object relationships and references

## Memory Management

### Garbage Collection

Automatic memory management via:

- **Generational Collector**: Optimized for short-lived objects
- **Concurrent Collection**: Minimal pause times
- **Memory Compaction**: Reduces fragmentation
- **Large Object Space**: Special handling for large allocations

Configuration options:

```bash
runavm --gc-initial-heap=128m --gc-max-heap=1g my_program.runab
```

### Memory Models

Configurable memory handling:

- **Standard**: Balanced performance and memory usage
- **Constrained**: Optimized for memory-limited environments
- **Server**: Optimized for high-throughput applications
- **Custom**: Fine-tuned for specific workloads

```bash
runavm --memory-model=server my_program.runab
```

### Memory Safety

Protection mechanisms:

- **Bounds Checking**: Prevention of buffer overflows
- **Use-After-Free Prevention**: Detection of dangling pointers
- **Type Safety**: Prevents invalid type conversions
- **Isolation**: Memory separation between components

## Concurrency Model

### Lightweight Concurrency

Efficient parallel execution:

- **Tasks**: Lightweight execution units (similar to goroutines)
- **Work Stealing**: Balanced distribution of computational work
- **Asynchronous I/O**: Non-blocking operations for improved throughput
- **Synchronization Primitives**: Mutexes, semaphores, channels

Example of task creation:

```
# Runa code
Process called perform_concurrent_work()
    Let tasks = List of Task of Integer()
    
    For i from 1 to 10
        tasks.add(Task.run(() => compute_value(i)))
    End For
    
    Let results = Task.await_all(tasks)
    Return results.sum()
End Process

# RunaVM execution handles task scheduling efficiently
```

### Structured Concurrency

Managed parallel execution:

- **Scoped Tasks**: Automatically managed lifetimes
- **Task Groups**: Collective operations on related tasks
- **Cancellation**: Structured cancellation propagation
- **Error Handling**: Coordinated error management

### Actor System

Message-passing concurrency:

- **Actors**: Isolated execution units with message queues
- **Supervisors**: Hierarchical failure handling
- **Location Transparency**: Consistent model across threads or nodes
- **Mailboxes**: Typed message passing between actors

## Interoperability

### Foreign Function Interface (FFI)

Integration with native code:

- **C/C++ Integration**: Direct calling of native functions
- **Bidirectional**: Call native code and be called from native code
- **Type Marshalling**: Automatic conversion between RunaVM and native types
- **Library Loading**: Dynamic loading of shared libraries

Example FFI declaration:

```
# Runa code with FFI
External Library "libc" 

External Process called printf(format as Pointer, args as Any) returns Integer from "libc"

Process called hello_world()
    Let message = "Hello, World!"
    printf("%s\n".to_c_string(), message.to_c_string())
End Process
```

### Platform Integration

Seamless integration with host platforms:

- **OS Services**: File system, networking, process management
- **GUI Integration**: Native UI components and frameworks
- **Hardware Access**: Device access where permitted
- **System Services**: Authentication, notifications, etc.

### Embedded Mode

RunaVM can be embedded in other applications:

- **Scriptable Applications**: Add Runa as a scripting layer
- **Extensibility**: Plugin systems based on Runa
- **Sandboxed Execution**: Secure execution of untrusted code

C API example for embedding:

```c
#include <runavm.h>

int main() {
    RunaVM* vm = runa_vm_create();
    
    // Configure VM
    runa_vm_set_memory_limit(vm, 100 * 1024 * 1024); // 100MB
    
    // Load and run code
    RunaStatus status = runa_vm_load_file(vm, "script.runab");
    if (status == RUNA_SUCCESS) {
        runa_vm_call_function(vm, "main", NULL, 0);
    }
    
    runa_vm_destroy(vm);
    return 0;
}
```

## Performance Optimization

### Just-In-Time Compilation

Dynamic optimization during execution:

- **Hot Spot Detection**: Identification of frequently executed code
- **Speculative Optimization**: Type specialization and inlining
- **Tiered Compilation**: Progressive optimization levels
- **Native Code Generation**: Direct execution on the CPU

JIT settings:

```bash
runavm --jit=on --jit-threshold=1000 my_program.runab
```

### Ahead-of-Time Compilation

Pre-compilation for faster startup:

- **Static Analysis**: Optimization based on whole-program analysis
- **Platform-Specific Code**: Target-specific optimizations
- **Reduced Startup Time**: Minimized initialization overhead
- **Smaller Memory Footprint**: Optimized code size

To use AOT compilation:

```bash
runa compile --aot my_program.runa
runavm --use-aot my_program.runab
```

### Profile-Guided Optimization

Data-driven performance improvements:

- **Execution Profiling**: Collection of runtime behavior data
- **Recompilation**: Optimization based on actual usage patterns
- **Branch Prediction**: Improved handling of conditional code
- **Cache Optimization**: Memory layout optimization for CPU caches

To use PGO:

```bash
# Generate profile
runavm --profile-gen my_program.runab

# Run with typical workload
# [... application runs normally ...]

# Use profile data for optimization
runavm --profile-use my_program.runab
```

## Security Features

### Sandboxing

Isolated execution environment:

- **Resource Limits**: Control over memory, CPU, and I/O usage
- **Capability Model**: Fine-grained permission system
- **Namespace Isolation**: Separated file system views
- **Network Restrictions**: Controlled network access

Enable sandbox:

```bash
runavm --sandbox --allow-fs=read:/data --allow-net=localhost:8080 my_program.runab
```

### Permission System

Granular security controls:

- **File System**: Read/write permissions by path
- **Network**: Connection restrictions by host/port
- **Process**: Creation and management of child processes
- **System**: Access to system information and services
- **User Data**: Access to user-specific information

### Security Policies

Configurable security rules:

- **Policy Files**: JSON-based security configurations
- **Defaults**: Built-in policies for common scenarios
- **Dynamic Adjustments**: Runtime policy modifications
- **Auditing**: Security event logging and monitoring

Example policy file:

```json
{
  "name": "restricted_web_service",
  "version": "1.0",
  "permissions": {
    "filesystem": {
      "allow": [
        {"path": "/app/data", "access": "read_write"},
        {"path": "/tmp", "access": "read_write"}
      ],
      "deny": [
        {"path": "/", "access": "all"}
      ]
    },
    "network": {
      "allow": [
        {"host": "localhost", "ports": "8000-9000"},
        {"host": "api.example.com", "ports": "443"}
      ]
    },
    "system": {
      "allow": ["time", "random", "environment"],
      "deny": ["process_creation", "device_access"]
    }
  }
}
```

## Deployment Options

### Standalone Execution

Run Runa applications directly:

- **Command Line**: Direct execution of bytecode files
- **Interactive Mode**: REPL for exploration and testing
- **Service Mode**: Long-running background services

Basic execution:

```bash
runavm my_program.runab
```

Interactive mode:

```bash
runavm --interactive
```

### Containerized Deployment

Packaged execution environments:

- **Docker Images**: Official RunaVM container images
- **Minimal Footprint**: Optimized for container environments
- **Configuration**: Environment-based VM settings
- **Multi-Stage Builds**: Separate build and runtime environments

Example Dockerfile:

```dockerfile
FROM runalang/runavm:latest

WORKDIR /app
COPY app.runab .
COPY config.json .

ENV RUNAVM_MEMORY_MAX="256m"
ENV RUNAVM_JIT="on"

EXPOSE 8080
CMD ["runavm", "--config", "config.json", "app.runab"]
```

### Cloud Deployment

Optimizations for cloud environments:

- **Serverless**: Quick startup for function-as-a-service
- **Scaling**: Efficient resource usage for variable loads
- **Monitoring**: Integration with cloud monitoring tools
- **State Management**: Options for persistent and ephemeral state

### Embedded Systems

RunaVM for constrained environments:

- **Memory Optimization**: Reduced footprint for limited RAM
- **Static Linking**: Self-contained executable for embedded targets
- **Hardware Interfaces**: Integration with device-specific features
- **Real-Time Options**: Configurations for timing-sensitive applications

Minimal mode:

```bash
runavm --embedded --memory-limit=16m --no-jit app.runab
```

## Troubleshooting

### Debugging

Tools for identifying and fixing issues:

- **Debugger**: Interactive debugging of running applications
- **Logging**: Configurable logging levels and destinations
- **Profiling**: CPU, memory, and I/O usage analysis
- **Tracing**: Detailed execution flow monitoring

Start debugging:

```bash
runavm --debug my_program.runab
```

### Common Issues

Solutions for frequent problems:

#### High Memory Usage

**Issue**: Application consumes excessive memory.

**Solutions**:
- Adjust garbage collection parameters:
  ```bash
  runavm --gc-young-size=20m --gc-collection-threshold=70 my_program.runab
  ```
- Enable memory profiling to identify leaks:
  ```bash
  runavm --profile-memory=heap.json my_program.runab
  ```

#### Slow Performance

**Issue**: Application runs slower than expected.

**Solutions**:
- Enable advanced JIT:
  ```bash
  runavm --jit=aggressive my_program.runab
  ```
- Use profile-guided optimization:
  ```bash
  runavm --profile-gen my_program.runab
  # Run typical workload
  runavm --profile-use my_program.runab
  ```

#### Startup Latency

**Issue**: Application takes too long to start.

**Solutions**:
- Use AOT compilation:
  ```bash
  runa compile --aot my_program.runa
  ```
- Create a snapshot for faster initialization:
  ```bash
  runavm --create-snapshot=app.snapshot --snapshot-main=initialize my_program.runab
  runavm --load-snapshot=app.snapshot my_program.runab
  ```

#### Compatibility Issues

**Issue**: Application works on one platform but not another.

**Solutions**:
- Use the compatibility mode:
  ```bash
  runavm --compat-mode=strict my_program.runab
  ```
- Check for platform-specific code:
  ```bash
  runavm --validate-portability my_program.runab
  ```

### Health Monitoring

Runtime health assessment:

- **Metrics**: Resource usage and performance statistics
- **Diagnostics**: Built-in diagnostic utilities
- **Remote Monitoring**: Integration with monitoring systems
- **Alerts**: Configurable thresholds and notifications

Enable monitoring server:

```bash
runavm --monitoring-port=8125 my_program.runab
```

## References

### Configuration Reference

Complete list of VM configuration options:

- **Runtime Options**: Memory, JIT, GC settings
- **Security Options**: Sandboxing and permissions
- **Debugging Options**: Logging, profiling, debugging
- **Performance Options**: Optimization and tuning

### VM Command Line Interface

RunaVM command syntax and options:

```
runavm [options] <program.runab> [program arguments]

Common options:
  --help                   Show help information
  --version                Display VM version
  --config <file>          Load configuration from file
  
Memory options:
  --memory-model <model>   Set memory model (standard, constrained, server)
  --gc-initial-heap <size> Set initial heap size (e.g., 128m)
  --gc-max-heap <size>     Set maximum heap size (e.g., 1g)
  
Performance options:
  --jit <mode>             JIT compilation mode (off, on, aggressive)
  --threads <count>        Number of worker threads (default: auto)
  --optimize <level>       Optimization level (0-3)
  
Security options:
  --sandbox                Enable sandbox mode
  --security-policy <file> Load security policy from file
  --allow-fs <spec>        Configure filesystem access
  --allow-net <spec>       Configure network access
  
Debugging options:
  --debug                  Enable debugger
  --log-level <level>      Set logging level (error, warn, info, debug, trace)
  --profile-cpu            Enable CPU profiling
  --profile-memory         Enable memory profiling
```

### Environment Variables

Configuration via environment:

| Variable | Description | Example |
|----------|-------------|---------|
| `RUNAVM_HOME` | Installation directory | `/opt/runavm` |
| `RUNAVM_LIBRARY_PATH` | Module search paths | `/app/lib:/usr/lib/runa` |
| `RUNAVM_MEMORY_MAX` | Maximum memory limit | `512m` |
| `RUNAVM_JIT` | JIT compilation mode | `on` |
| `RUNAVM_LOG_LEVEL` | Logging verbosity | `info` |
| `RUNAVM_CONFIG` | Configuration file path | `/etc/runavm/config.json` |
| `RUNAVM_SECURITY_POLICY` | Security policy path | `/etc/runavm/security.json` |

### Integration APIs

Developer resources for RunaVM integration:

- [C API Documentation](../API/RunaVM_C_API.md)
- [Embedding Guide](../Integration/Embedding_RunaVM.md)
- [Extension Development](../Development/VM_Extensions.md)
- [FFI Reference](../Integration/Foreign_Function_Interface.md) 