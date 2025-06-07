# Runa Bytecode Format Specification

This document specifies the format of Runa bytecode (`.runab`) files. The bytecode format is designed to be compact, efficient to load and execute, and to preserve the key semantic information needed for the RunaVM to execute code safely and efficiently.

## Table of Contents

1. [Overview](#overview)
2. [File Structure](#file-structure)
3. [Header Format](#header-format)
4. [Constant Pool](#constant-pool)
5. [Type Information](#type-information)
6. [Function Definitions](#function-definitions)
7. [Instruction Set](#instruction-set)
8. [Metadata Section](#metadata-section)
9. [Debug Information](#debug-information)
10. [Versioning](#versioning)
11. [Examples](#examples)
12. [Tools](#tools)
13. [References](#references)

## Overview

Runa bytecode is a binary representation of compiled Runa programs. Unlike some bytecode formats that discard type information, Runa bytecode preserves rich semantic information to enable:

- Runtime type checking
- Efficient garbage collection
- Just-in-time (JIT) compilation
- Dynamic optimization
- Comprehensive error reporting
- Advanced debugging features

The bytecode uses a stack-based execution model with register optimization and is designed to be efficiently executed by the RunaVM.

## File Structure

A `.runab` file contains the following sections in order:

```
┌────────────────────────────────────┐
│            Magic Number            │ (8 bytes)
├────────────────────────────────────┤
│             Header                 │ (Variable size)
├────────────────────────────────────┤
│          Constant Pool             │ (Variable size)
├────────────────────────────────────┤
│         Type Information           │ (Variable size)
├────────────────────────────────────┤
│       Function Definitions         │ (Variable size)
├────────────────────────────────────┤
│           Bytecode                 │ (Variable size)
├────────────────────────────────────┤
│         Metadata Section           │ (Variable size)
├────────────────────────────────────┤
│        Debug Information           │ (Optional, variable size)
└────────────────────────────────────┘
```

Each section begins with a 4-byte length indicator, followed by the section data.

## Header Format

The header contains general information about the bytecode file:

```
┌────────────────────────────────────┐
│            Magic Number            │ "RUNABYTC" (8 bytes)
├────────────────────────────────────┤
│           Format Version           │ (4 bytes - Major.Minor)
├────────────────────────────────────┤
│        Minimum VM Version          │ (4 bytes - Major.Minor)
├────────────────────────────────────┤
│         Creation Timestamp         │ (8 bytes - Unix timestamp)
├────────────────────────────────────┤
│            Flags                   │ (4 bytes)
├────────────────────────────────────┤
│         Source File Hash           │ (16 bytes - Optional)
├────────────────────────────────────┤
│      Required Native Libraries     │ (Variable size)
└────────────────────────────────────┘
```

### Flag Values

The flag values determine bytecode features and requirements:

| Flag | Hex Value | Description |
|------|-----------|-------------|
| HAS_DEBUG_INFO | 0x00000001 | Contains debug information |
| OPTIMIZED | 0x00000002 | Bytecode has been optimized |
| STRICT_TYPES | 0x00000004 | Enforce strict type checking |
| SANDBOXED | 0x00000008 | Requires sandbox execution |
| JIT_ALLOWED | 0x00000010 | Can be JIT-compiled |
| NATIVE_AOT | 0x00000020 | Contains AOT-compiled native code |
| REQUIRES_FFI | 0x00000040 | Requires FFI capabilities |
| SECURE_MEMORY | 0x00000080 | Uses secure memory operations |

## Constant Pool

The constant pool contains all literal values used in the program:

```
┌────────────────────────────────────┐
│      Constant Pool Size (N)        │ (4 bytes)
├────────────────────────────────────┤
│         Constant Type 1            │ (1 byte)
├────────────────────────────────────┤
│         Constant Data 1            │ (Variable size)
├────────────────────────────────────┤
│              ...                   │
├────────────────────────────────────┤
│         Constant Type N            │ (1 byte)
├────────────────────────────────────┤
│         Constant Data N            │ (Variable size)
└────────────────────────────────────┘
```

### Constant Types

| Type ID | Type Name | Format |
|---------|-----------|--------|
| 0x01 | Integer | 8-byte signed integer |
| 0x02 | Decimal | 8-byte IEEE 754 floating point |
| 0x03 | Boolean | 1-byte (0 = false, 1 = true) |
| 0x04 | Text | 4-byte length + UTF-8 encoded bytes |
| 0x05 | Null | No data |
| 0x06 | List | 4-byte count + constant pool indices of elements |
| 0x07 | Map | 4-byte count + (key, value) pairs of constant pool indices |
| 0x08 | Function Reference | 4-byte function ID |
| 0x09 | Type Reference | 4-byte type ID |
| 0x0A | External Reference | 4-byte length + name bytes + 4-byte library index |

## Type Information

The type information section describes all types used in the program:

```
┌────────────────────────────────────┐
│        Type Count (N)              │ (4 bytes)
├────────────────────────────────────┤
│          Type 1 Definition         │ (Variable size)
├────────────────────────────────────┤
│              ...                   │
├────────────────────────────────────┤
│          Type N Definition         │ (Variable size)
└────────────────────────────────────┘
```

### Type Definition Format

```
┌────────────────────────────────────┐
│          Type ID                   │ (4 bytes)
├────────────────────────────────────┤
│          Type Kind                 │ (1 byte)
├────────────────────────────────────┤
│          Type Name                 │ (4-byte length + UTF-8 bytes)
├────────────────────────────────────┤
│       Type-Specific Data           │ (Variable size based on Kind)
└────────────────────────────────────┘
```

### Type Kinds

| Kind ID | Kind | Type-Specific Data Format |
|---------|------|---------------------------|
| 0x01 | Primitive | None |
| 0x02 | Struct | 4-byte field count + field definitions |
| 0x03 | List | 4-byte type ID of element type |
| 0x04 | Map | 4-byte type ID of key type + 4-byte type ID of value type |
| 0x05 | Function | 4-byte param count + param type IDs + 4-byte return type ID |
| 0x06 | Optional | 4-byte type ID of base type |
| 0x07 | Union | 4-byte type count + type IDs |
| 0x08 | External | 4-byte length + layout metadata |

### Field Definition

```
┌────────────────────────────────────┐
│          Field Name                │ (4-byte length + UTF-8 bytes)
├────────────────────────────────────┤
│          Field Type ID             │ (4 bytes)
├────────────────────────────────────┤
│           Offset                   │ (4 bytes)
├────────────────────────────────────┤
│            Flags                   │ (1 byte)
└────────────────────────────────────┘
```

## Function Definitions

The function definitions section contains metadata for all functions in the program:

```
┌────────────────────────────────────┐
│        Function Count (N)          │ (4 bytes)
├────────────────────────────────────┤
│       Function 1 Definition        │ (Variable size)
├────────────────────────────────────┤
│              ...                   │
├────────────────────────────────────┤
│       Function N Definition        │ (Variable size)
└────────────────────────────────────┘
```

### Function Definition Format

```
┌────────────────────────────────────┐
│          Function ID               │ (4 bytes)
├────────────────────────────────────┤
│          Function Name             │ (4-byte length + UTF-8 bytes)
├────────────────────────────────────┤
│          Function Type ID          │ (4 bytes)
├────────────────────────────────────┤
│         Parameter Count            │ (4 bytes)
├────────────────────────────────────┤
│       Parameter Information        │ (Variable size based on count)
├────────────────────────────────────┤
│      Local Variable Count          │ (4 bytes)
├────────────────────────────────────┤
│     Local Variable Information     │ (Variable size based on count)
├────────────────────────────────────┤
│       Bytecode Offset              │ (4 bytes)
├────────────────────────────────────┤
│       Bytecode Length              │ (4 bytes)
├────────────────────────────────────┤
│            Flags                   │ (4 bytes)
└────────────────────────────────────┘
```

### Function Flags

| Flag | Hex Value | Description |
|------|-----------|-------------|
| EXTERNAL | 0x00000001 | Function is externally defined |
| NATIVE | 0x00000002 | Function has native implementation |
| CONSTRUCTOR | 0x00000004 | Function is a constructor |
| METHOD | 0x00000008 | Function is a method |
| ANONYMOUS | 0x00000010 | Anonymous function (e.g., lambda) |
| GENERATOR | 0x00000020 | Function is a generator |
| ASYNC | 0x00000040 | Function is asynchronous |
| VARARGS | 0x00000080 | Function accepts variable arguments |

### Parameter Information

For each parameter:

```
┌────────────────────────────────────┐
│          Parameter Name            │ (4-byte length + UTF-8 bytes)
├────────────────────────────────────┤
│          Parameter Type ID         │ (4 bytes)
├────────────────────────────────────┤
│            Flags                   │ (1 byte)
└────────────────────────────────────┘
```

### Local Variable Information

For each local variable:

```
┌────────────────────────────────────┐
│      Local Variable Name           │ (4-byte length + UTF-8 bytes)
├────────────────────────────────────┤
│      Local Variable Type ID        │ (4 bytes)
├────────────────────────────────────┤
│      Register/Slot Number          │ (2 bytes)
├────────────────────────────────────┤
│      Scope Start Offset            │ (4 bytes)
├────────────────────────────────────┤
│      Scope End Offset              │ (4 bytes)
└────────────────────────────────────┘
```

## Instruction Set

The bytecode section contains the actual instructions to be executed:

```
┌────────────────────────────────────┐
│        Bytecode Size               │ (4 bytes)
├────────────────────────────────────┤
│         Instruction 1              │ (Variable size)
├────────────────────────────────────┤
│              ...                   │
├────────────────────────────────────┤
│         Instruction N              │ (Variable size)
└────────────────────────────────────┘
```

### Instruction Format

Each instruction consists of an opcode followed by operands:

```
┌────────────────────────────────┐
│            Opcode              │ (1 byte)
├────────────────────────────────┤
│          Operand 1             │ (Size depends on opcode)
├────────────────────────────────┤
│             ...                │
├────────────────────────────────┤
│          Operand N             │ (Size depends on opcode)
└────────────────────────────────┘
```

### Core Opcodes

| Opcode | Hex | Name | Operands | Description |
|--------|-----|------|----------|-------------|
| 0x01 | NOP | None | No operation |
| 0x02 | PUSH_CONST | 2-byte constant pool index | Push constant onto stack |
| 0x03 | LOAD_LOCAL | 2-byte local variable index | Load local variable onto stack |
| 0x04 | STORE_LOCAL | 2-byte local variable index | Store stack top in local variable |
| 0x05 | LOAD_GLOBAL | 2-byte global variable index | Load global variable onto stack |
| 0x06 | STORE_GLOBAL | 2-byte global variable index | Store stack top in global variable |
| 0x07 | LOAD_FIELD | 2-byte field index | Load field from object on stack |
| 0x08 | STORE_FIELD | 2-byte field index | Store stack top in field of object |
| 0x09 | NEW | 4-byte type ID | Create new instance of type |
| 0x0A | CALL | 1-byte argument count | Call function on stack |
| 0x0B | CALL_METHOD | 2-byte method name index, 1-byte argument count | Call method on object |
| 0x0C | RETURN | None | Return from function |
| 0x0D | JUMP | 4-byte offset | Unconditional jump |
| 0x0E | JUMP_IF_TRUE | 4-byte offset | Jump if stack top is true |
| 0x0F | JUMP_IF_FALSE | 4-byte offset | Jump if stack top is false |
| 0x10 | ADD | None | Add top two stack items |
| 0x11 | SUB | None | Subtract stack top from stack second |
| 0x12 | MUL | None | Multiply top two stack items |
| 0x13 | DIV | None | Divide stack second by stack top |
| 0x14 | MOD | None | Modulo of stack second by stack top |
| 0x15 | NEG | None | Negate stack top |
| 0x16 | EQ | None | Compare stack top two items for equality |
| 0x17 | NE | None | Compare stack top two items for inequality |
| 0x18 | LT | None | Less than comparison |
| 0x19 | LE | None | Less than or equal comparison |
| 0x1A | GT | None | Greater than comparison |
| 0x1B | GE | None | Greater than or equal comparison |
| 0x1C | AND | None | Logical AND |
| 0x1D | OR | None | Logical OR |
| 0x1E | NOT | None | Logical NOT |
| 0x1F | DUP | None | Duplicate stack top |
| 0x20 | POP | None | Remove stack top |
| 0x21 | SWAP | None | Swap top two stack items |
| 0x22 | NEW_LIST | 1-byte element count | Create new list with elements from stack |
| 0x23 | NEW_MAP | 1-byte key-value pair count | Create new map with k-v pairs from stack |
| 0x24 | GET_ITEM | None | Get item at index (list) or key (map) |
| 0x25 | SET_ITEM | None | Set item at index or key |
| 0x26 | THROW | None | Throw exception from stack top |
| 0x27 | TRY_BEGIN | 4-byte catch offset, 4-byte finally offset | Begin try block |
| 0x28 | TRY_END | None | End try block |
| 0x29 | CATCH_BEGIN | 2-byte exception type index | Begin catch block |
| 0x2A | CATCH_END | None | End catch block |
| 0x2B | FINALLY_BEGIN | None | Begin finally block |
| 0x2C | FINALLY_END | None | End finally block |
| 0x2D | LOAD_UPVALUE | 2-byte upvalue index | Load from closure environment |
| 0x2E | STORE_UPVALUE | 2-byte upvalue index | Store to closure environment |
| 0x2F | CLOSURE | 4-byte function ID, 1-byte upvalue count + upvalue specs | Create function closure |
| 0x30 | TYPE_CHECK | 4-byte type ID | Check if stack top is of type |
| 0x31 | CAST | 4-byte type ID | Cast stack top to type |
| 0x32 | LOAD_MODULE | 2-byte module name index | Load module |
| 0x33 | IMPORT | 2-byte symbol count + symbol indices | Import symbols from module |

### Advanced Opcodes

| Opcode | Hex | Name | Operands | Description |
|--------|-----|------|----------|-------------|
| 0x40 | YIELD | None | Yield value from generator |
| 0x41 | AWAIT | None | Await async result |
| 0x42 | ITER_CREATE | None | Create iterator from iterable |
| 0x43 | ITER_NEXT | 4-byte end offset | Get next item from iterator |
| 0x44 | TYPEOF | None | Get type of stack top |
| 0x45 | INSTANCEOF | 4-byte type ID | Check if object is instance of type |
| 0x46 | LAMBDA | 1-byte capture count + capture specs | Create lambda function |
| 0x47 | SPREAD | None | Expand iterable into individual values |
| 0x48 | UNPACK | 1-byte element count | Unpack structure into individual values |
| 0x49 | SWITCH_TABLE | 4-byte case count + case values and offsets | Switch statement with jump table |
| 0x4A | INVOKE_FFI | 4-byte function reference | Call foreign function |
| 0x4B | INT_TO_DOUBLE | None | Convert integer to double |
| 0x4C | DOUBLE_TO_INT | None | Convert double to integer |
| 0x4D | TEXT_CONCAT | 1-byte string count | Concatenate strings |
| 0x4E | UNWIND | None | Unwind stack for exception |
| 0x4F | DEBUG_BREAK | 2-byte source line | Debugger breakpoint |

## Metadata Section

The metadata section contains additional information about the program:

```
┌────────────────────────────────────┐
│        Metadata Count (N)          │ (4 bytes)
├────────────────────────────────────┤
│       Metadata Entry 1 Type        │ (1 byte)
├────────────────────────────────────┤
│       Metadata Entry 1 Length      │ (4 bytes)
├────────────────────────────────────┤
│       Metadata Entry 1 Data        │ (Variable size)
├────────────────────────────────────┤
│              ...                   │
├────────────────────────────────────┤
│       Metadata Entry N Type        │ (1 byte)
├────────────────────────────────────┤
│       Metadata Entry N Length      │ (4 bytes)
├────────────────────────────────────┤
│       Metadata Entry N Data        │ (Variable size)
└────────────────────────────────────┘
```

### Metadata Types

| Type ID | Description | Format |
|---------|-------------|--------|
| 0x01 | Source File Path | UTF-8 string |
| 0x02 | Compiler Version | UTF-8 string |
| 0x03 | Compilation Options | JSON-encoded options |
| 0x04 | License Information | UTF-8 string |
| 0x05 | Module Dependencies | List of module references |
| 0x06 | Native Library Dependencies | List of library references |
| 0x07 | Author Information | UTF-8 string |
| 0x08 | Version String | UTF-8 string |
| 0x09 | Optimization Level | 1-byte value (0-3) |
| 0x0A | JIT Hints | Binary blob of JIT compiler hints |
| 0x0B | Security Requirements | JSON-encoded security requirements |

## Debug Information

If the `HAS_DEBUG_INFO` flag is set in the header, a debug information section follows:

```
┌────────────────────────────────────┐
│        Debug Info Size             │ (4 bytes)
├────────────────────────────────────┤
│       Source File Count (N)        │ (4 bytes)
├────────────────────────────────────┤
│        Source File 1 Entry         │ (Variable size)
├────────────────────────────────────┤
│              ...                   │
├────────────────────────────────────┤
│        Source File N Entry         │ (Variable size)
├────────────────────────────────────┤
│       Line Number Table Size       │ (4 bytes)
├────────────────────────────────────┤
│         Line Number Table          │ (Variable size)
├────────────────────────────────────┤
│     Local Variable Debug Info      │ (Variable size)
└────────────────────────────────────┘
```

### Source File Entry

```
┌────────────────────────────────────┐
│          File ID                   │ (4 bytes)
├────────────────────────────────────┤
│          File Path                 │ (4-byte length + UTF-8 bytes)
├────────────────────────────────────┤
│          Source Content Hash       │ (16 bytes - Optional)
└────────────────────────────────────┘
```

### Line Number Table

Maps bytecode offsets to source line numbers:

```
┌────────────────────────────────────┐
│          Entry Count (N)           │ (4 bytes)
├────────────────────────────────────┤
│       Bytecode Offset 1            │ (4 bytes)
├────────────────────────────────────┤
│          File ID 1                 │ (4 bytes)
├────────────────────────────────────┤
│       Line Number 1                │ (4 bytes)
├────────────────────────────────────┤
│       Column Number 1              │ (2 bytes)
├────────────────────────────────────┤
│              ...                   │
├────────────────────────────────────┤
│       Bytecode Offset N            │ (4 bytes)
├────────────────────────────────────┤
│          File ID N                 │ (4 bytes)
├────────────────────────────────────┤
│       Line Number N                │ (4 bytes)
├────────────────────────────────────┤
│       Column Number N              │ (2 bytes)
└────────────────────────────────────┘
```

## Versioning

The bytecode format uses a major.minor versioning scheme:

- Major version changes indicate incompatible changes
- Minor version changes indicate backwards-compatible additions

The current bytecode format version is 1.2.

Version history:
- 1.0: Initial release
- 1.1: Added support for generics and advanced type information
- 1.2: Added support for FFI, native code sections, and improved debug information

## Examples

### Simple Function Example

This example shows the bytecode representation of a simple function:

```
Process called add(a as Integer, b as Integer) returns Integer
    Return a + b
End Process
```

Bytecode representation (annotated):

```
# Function definition
Function ID: 1
Name: "add"
Type ID: 42 (Function(Integer, Integer) -> Integer)
Parameter Count: 2
  Parameter 1: Name="a", Type=Integer
  Parameter 2: Name="b", Type=Integer
Local Variable Count: 2
  Local 1: Name="a", Type=Integer, Register=0, Scope=0-12
  Local 2: Name="b", Type=Integer, Register=1, Scope=0-12
Bytecode Offset: 128
Bytecode Length: 12
Flags: 0

# Bytecode
LOAD_LOCAL 0     # Load parameter 'a'
LOAD_LOCAL 1     # Load parameter 'b'
ADD              # Add a + b
RETURN           # Return result
```

### More Complex Example

A more complex example showing a class with a method:

```
Class Person with
    Field name as Text
    Field age as Integer
    
    Process called initialize(name as Text, age as Integer)
        Self.name = name
        Self.age = age
    End Process
    
    Process called is_adult() returns Boolean
        Return Self.age >= 18
    End Process
End Class
```

Bytecode representation (partial):

```
# Type definition for Person
Type ID: 10
Type Kind: Struct
Type Name: "Person"
Field Count: 2
  Field 1: Name="name", Type=Text, Offset=0
  Field 2: Name="age", Type=Integer, Offset=8

# Function definition for initialize
Function ID: 5
Name: "initialize"
Type ID: 43 (Function(Person, Text, Integer) -> Void)
Parameter Count: 3
  Parameter 1: Name="self", Type=Person
  Parameter 2: Name="name", Type=Text
  Parameter 3: Name="age", Type=Integer
Local Variable Count: 3
  Local 1: Name="self", Type=Person, Register=0
  Local 2: Name="name", Type=Text, Register=1
  Local 3: Name="age", Type=Integer, Register=2
Bytecode Offset: 256
Bytecode Length: 24
Flags: METHOD | CONSTRUCTOR

# Bytecode for initialize
LOAD_LOCAL 0     # Load self
LOAD_LOCAL 1     # Load name parameter
STORE_FIELD 0    # Store in self.name field
LOAD_LOCAL 0     # Load self again
LOAD_LOCAL 2     # Load age parameter
STORE_FIELD 1    # Store in self.age field
LOAD_LOCAL 0     # Load self
RETURN           # Return self

# Function definition for is_adult
Function ID: 6
Name: "is_adult"
Type ID: 44 (Function(Person) -> Boolean)
Parameter Count: 1
  Parameter 1: Name="self", Type=Person
Local Variable Count: 1
  Local 1: Name="self", Type=Person, Register=0
Bytecode Offset: 280
Bytecode Length: 16
Flags: METHOD

# Bytecode for is_adult
LOAD_LOCAL 0     # Load self
LOAD_FIELD 1     # Load self.age
PUSH_CONST 5     # Push constant 18
GE               # Greater than or equal comparison
RETURN           # Return comparison result
```

## Tools

Runa provides several tools for working with bytecode files:

### Disassembler

The disassembler converts bytecode files to human-readable format:

```bash
runavm --disassemble program.runab
```

Sample output:

```
Function: main
Offset  Opcode        Operands       Line  Description
------  ------------  -------------  ----  ---------------------------
0000    PUSH_CONST    #5             10    Push constant "Hello, World!"
0003    STORE_GLOBAL  @2             10    Store in global 'message'
0006    LOAD_GLOBAL   @2             11    Load global 'message'
0009    CALL_METHOD   "length", 0    11    Call method with 0 args
0013    RETURN                       12    Return from function
```

### Bytecode Compiler

Direct compilation to bytecode:

```bash
runa compile --output program.runab program.runa
```

### Bytecode Verifier

Validates bytecode for correctness and safety:

```bash
runavm --verify program.runab
```

## References

- [RunaVM Instruction Set Reference](../API/RunaVM_Instruction_Set.md)
- [Runa Type System Specification](../Language/Type_System.md)
- [RunaVM Architecture](../Runtime/RunaVM.md)
- [Bytecode Optimization Guide](../Performance/Bytecode_Optimization.md) 