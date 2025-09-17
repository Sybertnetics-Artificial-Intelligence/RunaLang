# Runa Inline Assembly Specification

## Overview

Runa provides inline assembly capabilities that allow direct integration of assembly code within Runa functions. This feature is essential for:

- System calls and low-level OS interaction
- Performance-critical operations
- Hardware-specific instructions
- Memory management operations
- Self-hosting compiler implementation

## Syntax

The standardized syntax for inline assembly in Runa is:

```runa
Inline Assembly:
    "assembly instruction 1\n"    Note: Description of instruction 1
    "assembly instruction 2\n"    Note: Description of instruction 2
    "assembly instruction N\n"    Note: Description of instruction N
    : output_constraints
    : input_constraints  
    : clobber_list
End Assembly
```

**IMPORTANT**: Every assembly instruction line MUST have a `Note:` comment explaining what the instruction does. This is mandatory for code clarity and maintainability.

## Constraint Format

Runa uses GCC-style extended inline assembly constraints:

### Output Constraints
- **`"=r"(variable)`** - General-purpose register, output only
- **`"=m"(variable)`** - Memory location, output only
- **`"+r"(variable)`** - General-purpose register, input/output
- **`"+m"(variable)`** - Memory location, input/output

### Input Constraints  
- **`"r"(variable)`** - General-purpose register
- **`"m"(variable)`** - Memory operand
- **`"i"(constant)`** - Immediate integer constant
- **`"n"(constant)`** - Immediate integer constant with known numeric value

### Clobber List
- **Register names**: "rax", "rbx", "rcx", etc.
- **"memory"**: Indicates memory may be modified
- **"cc"**: Indicates condition codes may be modified

## Architecture Support

### x86_64 (Linux)
Primary target architecture with full support for:
- System calls via `syscall` instruction
- All general-purpose registers (rax, rbx, rcx, rdx, rsi, rdi, r8-r15)
- SSE and AVX instructions for performance
- Memory addressing modes

### ARM64 (Linux/macOS)
Secondary target with support for:
- System calls via `svc #0` instruction  
- General-purpose registers (x0-x30, w0-w30)
- NEON SIMD instructions
- Load/store addressing modes

### Other Architectures
Limited support planned for:
- RISC-V (future)
- x86 32-bit (compatibility)

## Common Patterns

### System Calls

```runa
Note: mmap syscall example
Let result as Integer
Inline Assembly:
    "mov rax, 9\n"       Note: mmap syscall number
    "mov rdi, %1\n"      Note: addr parameter
    "mov rsi, %2\n"      Note: length parameter  
    "mov rdx, %3\n"      Note: prot parameter
    "mov r10, %4\n"      Note: flags parameter
    "mov r8, %5\n"       Note: fd parameter
    "mov r9, %6\n"       Note: offset parameter
    "syscall\n"
    "mov %0, rax\n"      Note: Store result
    : "=r"(result)
    : "r"(addr), "r"(length), "r"(prot), "r"(flags), "r"(fd), "r"(offset)
    : "rax", "rcx", "r11", "memory"
End Assembly
```

### Memory Operations

```runa
Note: Fast memory copy
Inline Assembly:
    "mov rsi, %0\n"      Note: Source address
    "mov rdi, %1\n"      Note: Destination address
    "mov rcx, %2\n"      Note: Byte count
    "cld\n"              Note: Clear direction flag
    "rep movsb\n"        Note: Copy bytes
    :
    : "r"(src), "r"(dst), "r"(size)
    : "rsi", "rdi", "rcx", "memory"
End Assembly
```

### Atomic Operations

```runa
Note: Atomic compare-and-swap
Let success as Boolean
Inline Assembly:
    "mov rax, %2\n"      Note: Expected value
    "lock cmpxchg %3, %1\n"  Note: Compare and exchange
    "sete %0\n"          Note: Set result based on ZF flag
    : "=q"(success), "+m"(memory_location)
    : "r"(expected), "r"(new_value)
    : "rax", "memory", "cc"
End Assembly
```

### Performance Counters

```runa
Note: Read timestamp counter  
Let cycles as Integer
Inline Assembly:
    "rdtsc\n"           Note: Read time-stamp counter
    "shl rdx, 32\n"     Note: Shift high 32 bits
    "or rax, rdx\n"     Note: Combine high and low
    "mov %0, rax\n"     Note: Store result
    : "=r"(cycles)
    :
    : "rax", "rdx"
End Assembly
```

## Best Practices

### Security Considerations
1. **Validate all inputs** before passing to assembly
2. **Sanitize memory addresses** to prevent buffer overflows
3. **Use clobber lists correctly** to prevent register corruption
4. **Mark memory modifications** with "memory" clobber

### Performance Guidelines  
1. **Minimize register pressure** by using appropriate constraints
2. **Batch related operations** in single assembly blocks
3. **Use CPU-specific instructions** when beneficial (SIMD, etc.)
4. **Profile assembly code** to verify performance improvements

### Maintainability
1. **Document all assembly blocks** with clear comments
2. **Use meaningful variable names** in constraints
3. **Keep assembly blocks small** and focused
4. **Test thoroughly** on all target architectures

## Error Handling

### Common Errors
- **Invalid constraints**: Wrong constraint type for operand
- **Register conflicts**: Same register used for input/output without "+"
- **Missing clobbers**: Not listing modified registers
- **Incorrect syntax**: Malformed assembly instructions

### Debugging Tips
1. **Use objdump** to examine generated code
2. **Check constraint matching** between assembly and operands
3. **Verify syscall numbers** for target platform
4. **Test with simple examples** before complex operations

## Platform-Specific Details

### Linux x86_64 Syscalls
- System call numbers in `/usr/include/asm/unistd_64.h`
- Parameters passed in: rdi, rsi, rdx, r10, r8, r9
- Return value in rax (negative values indicate errors)
- Clobbered registers: rcx, r11

### Linux ARM64 Syscalls
- System call numbers in `/usr/include/asm-generic/unistd.h`
- Parameters passed in: x0-x7
- System call number in x8
- Return value in x0
- Use `svc #0` instruction

### macOS System Calls
- Different calling convention from Linux
- System call numbers offset by 0x2000000
- Additional error handling requirements
- Use `syscall` instruction on x86_64

## Integration with Runa

### Type Safety
- All assembly operands must have Runa type annotations
- Automatic size checking for register constraints
- Memory safety verification where possible

### Compiler Integration
- Assembly blocks are parsed during semantic analysis
- Register allocation considers inline assembly constraints
- Optimization passes preserve assembly semantics

### Runtime Behavior
- Assembly executes with same privileges as Runa code
- Memory model consistent with Runa's ownership system  
- Exception handling passes through assembly blocks

## Examples Repository

Complete examples are available in:
- `/runa/src/compiler/frontend/primitives/types/compiler_internals.runa`
- `/runa/src/compiler/backend/syscalls/syscall_generator.runa`
- `/runa/examples/inline_assembly/` (planned)

## Limitations

### Current Restrictions
- No nested inline assembly blocks
- Limited to GCC-style constraints
- x86_64 and ARM64 support only
- No inline assembly in constant expressions

### Future Enhancements
- RISC-V architecture support
- Enhanced constraint checking
- Assembly template macros
- Better debugging integration

## Conclusion

Inline assembly in Runa provides the low-level control necessary for system programming while maintaining type safety and integration with the language's ownership model. Use it judiciously for performance-critical code and system interface implementation.

For additional examples and advanced usage patterns, consult the Runa standard library implementation and compiler source code.