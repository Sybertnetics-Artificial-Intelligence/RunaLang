# RunaTime - Runa Runtime System

RunaTime is the resource management layer of the Runa language runtime, handling memory, concurrency, I/O, and system interfaces while delegating all code execution to the AOTT system.

## Philosophy

"RunaTime" reflects our belief that **runtime should be about time management** - managing the time your program spends on memory allocation, I/O operations, and system coordination, not code execution.

## Architecture

```
Application Code
       ↓
   [AOTT Execution] ←─────┐
       ↓                  │
   [RunaTime Services] ───┘
       ↓
   [Operating System]
```

## Directory Structure

- `bootstrap/` - Minimal Rust system interface (20%)
- `core/` - Core services (memory, types, objects) (Runa)
- `concurrency/` - Threading and async runtime (Runa)
- `io/` - File system and networking (Runa)
- `services/` - Runtime services and AOTT bridge (Runa)
- `integration/` - External system integration (Runa)

## Key Responsibilities

- **Memory Management**: Garbage collection, heap/stack management, allocators
- **Type System**: Runtime type information, reflection, dynamic dispatch
- **Concurrency**: Thread pools, async runtime, synchronization primitives
- **I/O Operations**: File system, networking, serialization
- **AOTT Bridge**: Interface between RunaTime and AOTT execution
- **System Integration**: FFI, process management, OS interfaces

## What RunaTime Does NOT Do

- **Code Execution**: All execution delegated to AOTT
- **Compilation**: Pure runtime system, no compilation
- **Static Analysis**: Handled by compiler

## Integration Points

- **Receives from**: Compiler (bytecode + metadata)
- **Delegates to**: AOTT (all code execution)
- **Provides to**: AOTT (memory, I/O, system services)

## Key Services

### Memory Management
- Garbage collector with generational collection
- Custom allocators for performance-critical paths
- Memory profiling and leak detection

### AOTT Bridge
- Execution coordination with AOTT tiers
- Profile data collection for optimization
- Tier transition management

### Concurrency Runtime
- Work-stealing thread pool
- Async/await executor
- Actor-based message passing

## Development Status

🚧 **Under Construction** - Fresh implementation as part of AOTT architecture rewrite.

See `../../docs/plans/RUNA_AOTT_ARCHITECTURE_PLAN.md` for full architectural context.