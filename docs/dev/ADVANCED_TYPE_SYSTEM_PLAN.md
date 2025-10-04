# Advanced Type System Implementation Plan
## "Better Than All" Type System Strategy

**Philosophy**: Beat Rust (safety), Python (simplicity), C (speed) - through progressive disclosure and opt-in complexity.

---

## 📋 Executive Summary

This plan implements a **hybrid type system** that maintains Runa's advantages while being competitive in all scenarios:

1. **Range-constrained integers** - Automatic optimization with bounds checking
2. **Float/Float64 types** - HPC performance with safe defaults
3. **Integer16/Integer32** - Explicit wire format types
4. **CInt/CLong/CSize** - Type-safe FFI
5. **Smart compiler warnings** - Detect wire format issues automatically

**Key Principle**: Automatic by default (ranges), explicit when needed (Integer16/32, FFI types).

---

## 🎯 Integration Points with Existing Roadmap

### Phase 1: Foundation (v0.0.8.6 - NEW)
**Timing**: After v0.0.8.5 (String Interpolation), Before v0.0.9 (Error Handling)

**Why here**:
- Struct construction (v0.0.8.1) is complete ✅
- Collections (v0.0.8.2) benefit from range-optimized indexes
- Pattern matching (v0.0.8.3) can use ranges in patterns
- Lambda/inference (v0.0.8.4) needs good type foundation
- Error handling (v0.0.9) needs robust type system underneath

**Dependencies**:
- ✅ v0.0.8.1: Struct construction (type registry exists)
- ✅ v0.0.8: Basic type system (Integer, Pointer, String)

---

## 🚨 Critical Issues That Must Be Fixed First

### Issue 1: Sign Extension Bug (v0.0.8.0.5 - BLOCKING)

**Status**: ❌ **BLOCKING** - Must fix before implementing advanced types

**The Problem**:
```c
// runtime.c (current):
int32_t memory_get_int32(void* ptr, int64_t offset) {
    return *(int32_t*)((char*)ptr + offset);  // Returns int32_t (4 bytes)
}
// C compiler implicitly converts int32_t → int64_t with sign extension (usually works)

// BUT the generated assembly does:
movl (%rax), %eax    # ZERO-extends, not sign-extends!
ret
```

**The Bug**:
- `movl` zeros upper 32 bits of `%rax`
- Negative int32 values become huge positive int64 values
- Example: -1 (0xFFFFFFFF) becomes 4294967295 (0x00000000FFFFFFFF)

**The Fix**:

**Option A: Fix in runtime.c** (Recommended - simplest):
```c
int64_t memory_get_int32(void* ptr, int64_t offset) {  // Change return type
    int32_t value = *(int32_t*)((char*)ptr + offset);
    return (int64_t)value;  // Explicit sign-extension
}
```

**Option B: Fix in generated assembly**:
```asm
# Replace:
movl (%rax), %eax

# With:
movslq (%rax), %rax   # Move with Sign-extension Long to Quad
```

**Files to Fix**:
1. `runtime/runtime.c` - Change return type to `int64_t`, explicit cast
2. Recompile runtime with fix
3. Test with negative values

**Test Case**:
```runa
# test_sign_extension.runa
Process called "test_negative_int32" returns Integer:
    Let buffer be allocate(8)
    memory_set_int32(buffer, 0, -42)
    Let retrieved be memory_get_int32(buffer, 0)
    If retrieved is not equal to -42:
        display("FAIL: Expected -42, got ")
        display(integer_to_string(retrieved))
        Return -1
    End If
    Return 0  # Success
End Process
```

**Impact**: Without this fix, **all int32 usage is broken** (struct field offsets, type IDs, sizes, etc.)

---

### Issue 2: Stack Offsets (Currently Not Broken, But Will Be)

**Status**: ⚠️ Not a bug NOW, but will become a bug with variable-sized types

### The Problem:

**Current codegen (v0.0.8.1) assumes all variables are 8 bytes:**
```runa
# In codegen_generate_process():
Let offset be variable_count multiplied by 8  # HARDCODED 8!
```

**This breaks with variable-sized types:**
```runa
Process called "example":
    Let a as Integer range 0 to 255      # 1 byte
    Let b as Integer range 0 to 65535    # 2 bytes
    Let c as Integer                     # 8 bytes
End Process

# Current (WRONG):
# a at offset 0  (1 byte, but reserves 8)
# b at offset 8  (2 bytes, but reserves 8)
# c at offset 16 (8 bytes, correct by accident)
# Total: 24 bytes (wastes 13 bytes!)

# Correct:
# a at offset 0  (1 byte)
# b at offset 2  (2 bytes, aligned)
# c at offset 8  (8 bytes, aligned)
# Total: 16 bytes (optimal, no waste)
```

### The Solution:

**Replace all hardcoded `multiplied by 8` with actual size calculation:**

1. **Track variable sizes** during parsing:
   ```runa
   Type called "Variable":
       name as Pointer
       type as Pointer        # Now includes range info!
       size as Integer        # Computed from type
       alignment as Integer   # Computed from type
       offset as Integer      # Computed during layout
   End Type
   ```

2. **Compute stack layout** in codegen:
   ```runa
   Process called "compute_stack_layout" takes variables as Pointer, count as Integer returns Integer:
       Let current_offset be 0
       Let i be 0
       While i is less than count:
           Let var be get_variable(variables, i)
           Let size be get_variable_size(var)
           Let align be get_variable_alignment(var)

           Note: Align current offset
           Let remainder be current_offset modulo by align
           If remainder is not equal to 0:
               Set current_offset to current_offset plus (align minus remainder)
           End If

           Note: Assign offset to variable
           set_variable_offset(var, current_offset)

           Note: Advance offset
           Set current_offset to current_offset plus size
           Set i to i plus 1
       End While

       Note: Return total stack space needed (aligned to 16 bytes for call convention)
       Let remainder be current_offset modulo by 16
       If remainder is not equal to 0:
           Set current_offset to current_offset plus (16 minus remainder)
       End If
       Return current_offset
   End Process
   ```

3. **Use correct load/store instructions**:
   ```runa
   Process called "codegen_load_variable" takes codegen as Integer, var as Integer:
       Let size be get_variable_size(var)
       Let offset be get_variable_offset(var)
       Let output be get_codegen_output(codegen)

       If size is equal to 1:
           # 8-bit load - NEED TO HANDLE SIGNED VS UNSIGNED!
           Let is_signed be get_variable_signed(var)
           If is_signed is equal to 1:
               file_write_buffered(output, "    movsbq -", 0)  # Sign-extend
           Otherwise:
               file_write_buffered(output, "    movzbq -", 0)  # Zero-extend
           End If
           file_write_buffered(output, integer_to_string(offset), 0)
           file_write_buffered(output, "(%rbp), %rax\n", 0)
       Otherwise If size is equal to 2:
           # 16-bit load - NEED TO HANDLE SIGNED VS UNSIGNED!
           Let is_signed be get_variable_signed(var)
           If is_signed is equal to 1:
               file_write_buffered(output, "    movswq -", 0)  # Sign-extend
           Otherwise:
               file_write_buffered(output, "    movzwq -", 0)  # Zero-extend
           End If
           file_write_buffered(output, integer_to_string(offset), 0)
           file_write_buffered(output, "(%rbp), %rax\n", 0)
       Otherwise If size is equal to 4:
           # 32-bit load - NEED TO HANDLE SIGNED VS UNSIGNED!
           Let is_signed be get_variable_signed(var)
           If is_signed is equal to 1:
               file_write_buffered(output, "    movslq -", 0)  # Sign-extend
           Otherwise:
               file_write_buffered(output, "    movl -", 0)    # Zero-extend (implicit)
           End If
           file_write_buffered(output, integer_to_string(offset), 0)
           file_write_buffered(output, "(%rbp), %eax\n", 0)
       Otherwise:
           # 64-bit load
           file_write_buffered(output, "    movq -", 0)
           file_write_buffered(output, integer_to_string(offset), 0)
           file_write_buffered(output, "(%rbp), %rax\n", 0)
       End If
   End Process

   Process called "codegen_store_variable" takes codegen as Integer, var as Integer:
       Let size be get_variable_size(var)
       Let offset be get_variable_offset(var)
       Let output be get_codegen_output(codegen)

       If size is equal to 1:
           # 8-bit store
           file_write_buffered(output, "    movb %al, -", 0)
           file_write_buffered(output, integer_to_string(offset), 0)
           file_write_buffered(output, "(%rbp)\n", 0)
       Otherwise If size is equal to 2:
           # 16-bit store
           file_write_buffered(output, "    movw %ax, -", 0)
           file_write_buffered(output, integer_to_string(offset), 0)
           file_write_buffered(output, "(%rbp)\n", 0)
       Otherwise If size is equal to 4:
           # 32-bit store
           file_write_buffered(output, "    movl %eax, -", 0)
           file_write_buffered(output, integer_to_string(offset), 0)
           file_write_buffered(output, "(%rbp)\n", 0)
       Otherwise:
           # 64-bit store
           file_write_buffered(output, "    movq %rax, -", 0)
           file_write_buffered(output, integer_to_string(offset), 0)
           file_write_buffered(output, "(%rbp)\n", 0)
       End If
   End Process
   ```

### Files That Need Changes:

1. **parser.runa**:
   - Track type info (including ranges) with variables
   - Store size/alignment in variable metadata

2. **codegen.runa**:
   - Replace ALL `multiplied by 8` with `get_variable_offset()`
   - Add `compute_stack_layout()` process
   - Add `codegen_load_variable()` and `codegen_store_variable()` helpers
   - Use size-specific instructions (movb/movw/movl/movq)

3. **type_system.runa** (new file):
   - `get_type_size()` - Returns 1/2/4/8 based on type
   - `get_type_alignment()` - Returns alignment requirement
   - `get_type_signed()` - Returns 1 if signed, 0 if unsigned
   - `compute_range_size()` - Determines bytes needed for range (MUST handle signed vs unsigned!)
   - `compute_range_signedness()` - Returns 1 if range includes negative values

### Impact:

**Without this fix:**
- ❌ Range constraints waste memory (always allocate 8 bytes)
- ❌ Stack corruption possible (wrong offsets)
- ❌ Performance penalty (unnecessary memory usage)

**With this fix:**
- ✅ Optimal memory usage (1/2/4/8 bytes as needed)
- ✅ Correct stack layout (proper alignment)
- ✅ Fast access (size-appropriate instructions)

### Testing:

**CRITICAL TEST**: `test_stack_layout.runa` (see Phase 1A test cases above)
- Verifies variables with different sizes don't corrupt each other
- Ensures alignment is correct
- Confirms total stack space is minimized

---

## 📐 Implementation Phases

### **Phase 1A: Range-Constrained Integers (v0.0.8.6)**
**Timeline**: 2-3 weeks
**Priority**: CRITICAL - Foundation for everything else

#### Parser Changes:
```runa
# New syntax:
Let age as Integer range 0 to 150
Let temperature as Integer range -200 to 200
Let port as Integer range 0 to 65535
```

**Implementation**:
1. **Lexer** (minimal changes):
   - `range` is already a potential keyword, no new tokens needed
   - `to` is already TOKEN_TO (exists)

2. **Parser** (parser.runa):
   - Extend `parser_parse_type()` to recognize `range MIN to MAX`
   - Create `TYPE_INTEGER_RANGED` (new type kind)
   - Store min/max in type metadata

   ```runa
   Note: In parser_parse_type()
   If type_name equals "Integer":
       Let current_token be memory_get_pointer(parser, 8)
       Let token_type be memory_get_integer(current_token, 0)
       If token_type is equal to TOKEN_RANGE:
           parser_eat(parser, TOKEN_RANGE)
           Let min_value be parser_parse_expression(parser)
           parser_expect(parser, TOKEN_TO)
           Let max_value be parser_parse_expression(parser)
           Note: Create ranged integer type with constraints
           Return create_ranged_integer_type(min_value, max_value)
       End If
   End If
   ```

3. **Type System** (new: type_system.runa):
   ```runa
   Type called "RangedIntegerType":
       base_type as Integer       # TYPE_INTEGER
       min_value as Integer
       max_value as Integer
       computed_size as Integer   # 1, 2, 4, or 8 bytes
   End Type

   Process called "compute_range_size" takes min as Integer, max as Integer returns Integer:
       Let range be max minus min
       If range is less than 256:
           Return 1  # 8-bit
       Otherwise If range is less than 65536:
           Return 2  # 16-bit
       Otherwise If range is less than 4294967296:
           Return 4  # 32-bit
       Otherwise:
           Return 8  # 64-bit
       End If
   End Process
   ```

4. **Codegen** (codegen.runa):
   - **CRITICAL: Stack Offset Calculation** (THIS WAS MISSING!)
   ```runa
   Note: OLD (WRONG) - assumes all variables are 8 bytes:
   Let offset be variable_count multiplied by 8

   Note: NEW (CORRECT) - compute actual offsets:
   Process called "compute_stack_layout" takes variables as Pointer, count as Integer returns Pointer:
       Let layout be memory_allocate(count multiplied by 16)  # [offset, size] pairs
       Let current_offset be 0
       Let i be 0
       While i is less than count:
           Let var be memory_get_pointer(variables, i multiplied by 8)
           Let var_type be get_variable_type(var)
           Let var_size be get_type_size(var_type)
           Let var_align be get_type_alignment(var_type)

           Note: Align current offset
           Let remainder be current_offset modulo by var_align
           If remainder is not equal to 0:
               Set current_offset to current_offset plus (var_align minus remainder)
           End If

           Note: Store offset and size
           memory_set_integer(layout, i multiplied by 16, current_offset)
           memory_set_integer(layout, (i multiplied by 16) plus 8, var_size)

           Note: Advance offset
           Set current_offset to current_offset plus var_size
           Set i to i plus 1
       End While
       Return layout
   End Process
   ```

   - Generate bounds checks on assignment:
   ```runa
   Note: For "Set x to value" where x has range [0, 100]:
   # Generated assembly:
   cmpq $0, %rax
   jl .bounds_error
   cmpq $100, %rax
   jg .bounds_error
   # ... normal assignment ...
   ```

   - Use optimized storage with correct offsets:
   ```runa
   Note: For Integer range 0 to 255 (1 byte) at stack offset X:
   movb %al, -X(%rbp)    # Store 1 byte at computed offset

   Note: For Integer range 0 to 65535 (2 bytes) at stack offset Y:
   movw %ax, -Y(%rbp)    # Store 2 bytes at computed offset

   Note: Offsets are NO LONGER multiples of 8!
   ```

   - **Alignment Requirements**:
   ```runa
   Note: Alignment rules (x86-64):
   Integer (8 bytes) → 8-byte alignment
   Integer32 (4 bytes) → 4-byte alignment
   Integer16 (2 bytes) → 2-byte alignment
   Integer range (1 byte) → 1-byte alignment
   Float (4 bytes) → 4-byte alignment
   Float64 (8 bytes) → 8-byte alignment
   ```

5. **Runtime** (runtime/runtime.c):
   - Add bounds check error handler:
   ```c
   void bounds_check_failed(int64_t value, int64_t min, int64_t max) {
       fprintf(stderr, "[RUNTIME ERROR] Value %ld out of range [%ld, %ld]\n",
               value, min, max);
       exit(1);
   }
   ```

#### Success Criteria:
- ✅ `Integer range MIN to MAX` syntax parses correctly
- ✅ Compiler computes optimal size (1/2/4/8 bytes)
- ✅ Bounds checks inserted on assignment
- ✅ Runtime panics on out-of-range values with clear message
- ✅ Struct fields with ranges use optimized storage
- ✅ Tests pass for all range sizes

#### Test Cases:
```runa
# test_range_basic.runa
Let small as Integer range 0 to 10
Set small to 5      # OK
Set small to 20     # Runtime error

# test_range_struct.runa
Type called "Sensor":
    temperature as Integer range -200 to 200   # 2 bytes
    humidity as Integer range 0 to 100         # 1 byte
    timestamp as Integer                       # 8 bytes (no range)
End Type

Let sensor be a value of type Sensor with temperature as 25 and humidity as 60 and timestamp as 1000000

# test_range_negative.runa
Let offset as Integer range -1000 to 1000     # Signed, 2 bytes
Set offset to -500  # OK
Set offset to 2000  # Runtime error

# test_stack_layout.runa (CRITICAL - tests stack offsets!)
Process called "test_mixed_sizes" returns Integer:
    Let a as Integer range 0 to 255           # 1 byte at offset 0
    Let b as Integer range 0 to 65535         # 2 bytes at offset 2 (aligned)
    Let c as Integer                          # 8 bytes at offset 8 (aligned)
    Let d as Integer range 0 to 100           # 1 byte at offset 16

    Set a to 10
    Set b to 1000
    Set c to 123456789
    Set d to 50

    # Verify all values are independent (no overlap)
    If a is not equal to 10:
        Return -1
    End If
    If b is not equal to 1000:
        Return -2
    End If
    If c is not equal to 123456789:
        Return -3
    End If
    If d is not equal to 50:
        Return -4
    End If

    Return 0  # Success
End Process

# test_struct_field_offsets.runa (CRITICAL - tests struct layout!)
Type called "MixedSize":
    tiny as Integer range 0 to 255            # 1 byte at offset 0
    small as Integer range 0 to 65535         # 2 bytes at offset 2 (aligned)
    large as Integer                          # 8 bytes at offset 8 (aligned)
End Type

Let mixed be a value of type MixedSize with tiny as 5 and small as 500 and large as 999999

# Access each field independently
Let t be the tiny of mixed       # Should be 5
Let s be the small of mixed      # Should be 500
Let l be the large of mixed      # Should be 999999
```

---

### **Phase 1B: Float Types (v0.0.8.6)**
**Timeline**: 1-2 weeks (parallel with ranges)
**Priority**: HIGH - Essential for HPC

#### Parser Changes:
```runa
# New types:
Let position as Float        # 32-bit (4 bytes)
Let precise as Float64       # 64-bit (8 bytes) - DEFAULT for safety
```

**Implementation**:
1. **Lexer**:
   - Add TOKEN_FLOAT keyword
   - Add TOKEN_FLOAT64 keyword
   - Float literals: `3.14` → TOKEN_FLOAT_LITERAL

2. **Parser**:
   - Add TYPE_FLOAT and TYPE_FLOAT64 to type system
   - Parse float literals
   ```runa
   Process called "parser_parse_float_literal" takes parser as Integer returns Integer:
       Let token be memory_get_pointer(parser, 8)
       Let value_str be memory_get_pointer(token, 8)
       Let float_value be string_to_float(value_str)
       Let expr be memory_allocate(16)
       memory_set_integer(expr, 0, EXPR_FLOAT_LITERAL)
       memory_set_float(expr, 8, float_value)
       Return expr
   End Process
   ```

3. **Codegen**:
   - Use SSE/AVX registers for float operations:
   ```runa
   Note: Float32 operations use xmm registers
   movss value(%rip), %xmm0      # Load float
   addss other(%rip), %xmm0      # Add floats
   movss %xmm0, result(%rip)     # Store float

   Note: Float64 operations use xmm registers (64-bit)
   movsd value(%rip), %xmm0      # Load double
   addsd other(%rip), %xmm0      # Add doubles
   movsd %xmm0, result(%rip)     # Store double
   ```

4. **Runtime**:
   - Add float conversion functions:
   ```c
   float string_to_float(const char* str);
   char* float_to_string(float value);
   double string_to_float64(const char* str);
   char* float64_to_string(double value);
   ```

#### Success Criteria:
- ✅ Float and Float64 types parse correctly
- ✅ Float literals work: `3.14`, `2.5e-3`
- ✅ Arithmetic operations: `+`, `-`, `*`, `/`
- ✅ Comparisons: `<`, `>`, `<=`, `>=`, `==`
- ✅ Conversion: Integer to Float, Float to Integer
- ✅ Struct fields can be Float/Float64
- ✅ HPC use case: particle simulation performs on par with C

#### Test Cases:
```runa
# test_float_basic.runa
Let x as Float be 3.14
Let y as Float be 2.5
Let sum be x plus y
display(sum)  # 5.64

# test_float_struct.runa (HPC use case)
Type called "Particle":
    x as Float
    y as Float
    z as Float
    vx as Float
    vy as Float
    vz as Float
End Type

Let p be a value of type Particle with x as 1.0 and y as 2.0 and z as 3.0 and vx as 0.1 and vy as 0.2 and vz as 0.3

# test_float_precision.runa
Let precise as Float64 be 1.23456789012345
Let approx as Float be 1.23456789012345
Note: Float64 maintains precision, Float does not
```

---

### **Phase 2: Explicit Wire Format Types (v0.0.8.7 - NEW)**
**Timeline**: 1 week
**Priority**: MEDIUM - Needed for network protocols

**Timing**: After Phase 1 (ranges + floats work)

#### New Types:
```runa
Integer16    # Always 2 bytes, signed
Integer32    # Always 4 bytes, signed
UInteger16   # Always 2 bytes, unsigned
UInteger32   # Always 4 bytes, unsigned
```

**Implementation**:
1. **Parser**:
   - Add new type keywords
   - These are **fixed-size**, no range allowed

2. **Type System**:
   ```runa
   Let TYPE_INTEGER16 be 10
   Let TYPE_INTEGER32 be 11
   Let TYPE_UINTEGER16 be 12
   Let TYPE_UINTEGER32 be 13
   ```

3. **Codegen**:
   - Fixed sizes, no bounds checks (explicit contract)
   ```runa
   Note: Integer16 always uses 16-bit operations
   movw %ax, offset(%rbp)    # Store 2 bytes

   Note: Integer32 always uses 32-bit operations
   movl %eax, offset(%rbp)   # Store 4 bytes
   ```

#### Wire Format Syntax (Optional Enhancement):
```runa
# Optional: Explicit wire format annotation
Type called "TcpPacket" for network protocol:
    src_port as Integer16     # Locked at 2 bytes
    dst_port as Integer16
    sequence as Integer32
    ack as Integer32
End Type

# Compiler guarantees:
# - Size never changes
# - Layout is stable
# - No padding (explicit control)
```

#### Success Criteria:
- ✅ Integer16/Integer32 types work
- ✅ Unsigned variants work (UInteger16/32)
- ✅ Binary serialization works (zero-copy)
- ✅ Network protocol example compiles and runs
- ✅ No accidental size changes (stable ABI)

#### Test Cases:
```runa
# test_wire_format.runa
Type called "Packet":
    packet_id as Integer16
    sequence as Integer32
    checksum as Integer16
End Type

Let pkt be a value of type Packet with packet_id as 1 and sequence as 1000 and checksum as 42

# Verify size:
Let size be sizeof_type("Packet")
If size is not equal to 8:
    panic("Packet size changed!")
End If

# test_network_send.runa
Process called "send_packet" takes pkt as Packet returns Integer:
    # Zero-copy: send struct directly as bytes
    Return network_write(pkt as Pointer, 8)
End Process
```

---

### **Phase 3: FFI Types (v0.0.9)**
**Timeline**: 1 week
**Priority**: MEDIUM - Needed for C library interop

**Timing**: Integrate with v0.0.9 (Error Handling + Generics)

#### New Types:
```runa
CInt      # Matches C's int (typically 32-bit)
CLong     # Matches C's long (64-bit on Linux, 32-bit on Windows)
CSize     # Matches C's size_t (pointer-sized)
CChar     # Matches C's char (8-bit)
```

**Implementation**:
1. **Parser**:
   - Add FFI type keywords
   - Mark processes that use FFI types (for safety)
   ```runa
   Process called "call_c_function" calling C library takes fd as CInt returns CInt:
       # ...
   End Process
   ```

2. **Type System**:
   - Platform-specific sizes:
   ```runa
   Note: On Linux x86-64:
   CInt = 32-bit
   CLong = 64-bit
   CSize = 64-bit

   Note: On Windows x86-64:
   CInt = 32-bit
   CLong = 32-bit (!!)
   CSize = 64-bit
   ```

3. **Codegen**:
   - Enforce conversion at FFI boundary:
   ```runa
   # Must explicitly convert:
   Let runa_value as Integer be 100
   Let c_value as CInt be runa_value as CInt   # Explicit cast required
   ```

4. **Compiler Warnings**:
   ```
   Warning: Mixing Integer and CInt without explicit conversion
   Help: Use "value as CInt" to convert
   ```

#### Success Criteria:
- ✅ FFI types match platform C types
- ✅ Explicit conversion required (no implicit mixing)
- ✅ Calling C functions works correctly
- ✅ Platform differences handled correctly
- ✅ Tests pass on Linux and Windows

#### Test Cases:
```runa
# test_ffi_basic.runa
External Process called "open" calling C library takes path as Pointer, flags as CInt returns CInt

Process called "test_open" returns Integer:
    Let flags as CInt be 0  # O_RDONLY
    Let fd as CInt be open("/tmp/test.txt" as Pointer, flags)
    If fd is less than 0:
        Return -1
    End If
    Return fd as Integer  # Explicit conversion back
End Process

# test_ffi_mixing_error.runa
Let x as Integer be 100
Let y as CInt be 50
Let z be x plus y  # Compiler ERROR: Cannot mix Integer and CInt
```

---

### **Phase 4: Smart Compiler Warnings (v0.0.9)**
**Timeline**: 1 week (parallel with Phase 3)
**Priority**: LOW - Nice to have

#### Warning 1: Potential Wire Format
```runa
# Code:
Type called "NetworkPacket":
    id as Integer range 0 to 65535
End Type

# Warning:
# "NetworkPacket has network-related name but uses automatic sizing.
#  Consider Integer16 for stable wire format, or rename if not for network."
```

**Implementation**:
- Pattern match type names: "Packet", "Protocol", "Message", "Frame"
- Suggest Integer16/32 if ranges fit

#### Warning 2: Range Changed (Breaking Change Detection)
```runa
# Version 1.0:
Type called "Config":
    port as Integer range 0 to 65535  # 2 bytes

# Version 1.1 (change):
Type called "Config":
    port as Integer range 0 to 100000  # NOW 4 bytes!

# Compiler ERROR:
# "Config.port range changed from [0,65535] to [0,100000], causing size change 2→4 bytes.
#  This breaks binary compatibility!
#  Options:
#    1. Revert range to [0,65535]
#    2. Use explicit Integer32
#    3. Add annotation: Note: BREAKING CHANGE v1.1"
```

**Implementation**:
- Store type metadata in `.runa-meta` file
- Compare on recompilation
- Error if struct size changes without annotation

#### Warning 3: Serialization Detection
```runa
# Code:
Process called "send_message" takes msg as Message:
    network_send(msg as Pointer, sizeof_type("Message"))
End Process

# Warning:
# "Message is serialized to bytes but uses automatic sizing.
#  Consider explicit Integer16/32 for stable wire format."
```

**Implementation**:
- Detect `as Pointer` casts on struct types
- Detect calls to network/file write functions
- Suggest explicit types

---

## 🔮 Missing Pieces: What the Plan Doesn't Cover (YET)

### Gap 1: Signed vs Unsigned Range Size Computation ⚠️ CRITICAL

**Current `compute_range_size()` is too simplistic**:
```runa
# Current (WRONG):
Let range be max minus min
If range is less than 256:
    Return 1  # WRONG for signed!
```

**Need**:
```runa
Process called "compute_range_size" takes min as Integer, max as Integer returns Integer:
    If min is less than 0:
        # Signed range
        If min >= -128 and max <= 127: Return 1
        Otherwise If min >= -32768 and max <= 32767: Return 2
        Otherwise If min >= -2147483648 and max <= 2147483647: Return 4
        Otherwise: Return 8
    Otherwise:
        # Unsigned range
        If max <= 255: Return 1
        Otherwise If max <= 65535: Return 2
        Otherwise If max <= 4294967295: Return 4
        Otherwise: Return 8
    End If
End Process
```

**Add to Phase 1A checklist**.

---

### Gap 2: Arithmetic Promotion Rules ⚠️ HIGH PRIORITY

**Problem**:
```runa
Let a as Integer range 0 to 100
Let b as Integer range 0 to 100
Let c be a plus b    # Result: 0 to 200? Full Integer? What?
```

**Solution Options**:
- **Option A** (Simple): Promote to full Integer (8 bytes)
- **Option B** (Complex): Infer new range [0, 200]

**Recommendation**: Start with Option A (v0.0.8.6), add Option B later (v0.1.0+).

**Add to Phase 1A success criteria**: "Arithmetic on ranged integers promotes to full Integer".

---

### Gap 3: Compile-Time Range Verification ⚠️ HIGH PRIORITY

**Problem**:
```runa
Let x as Integer range 0 to 100 be 200    # Should be COMPILE error, not runtime!
```

**Need**:
```runa
Process called "verify_literal_in_range" takes value as Integer, min as Integer, max as Integer:
    If value < min or value > max:
        emit_compile_error("Literal value out of range")
    End If
End Process
```

**Add to Phase 1A**: Compile-time verification for literal assignments.

---

### Gap 4: Overflow Behavior in Arithmetic 🔄 DESIGN DECISION NEEDED

**Problem**:
```runa
Let x as Integer range 0 to 100 be 50
Let y as Integer range 0 to 100 be 80
Let z as Integer range 0 to 100 be x plus y    # 130 > 100!
```

**Options**:
- **A**: Panic at assignment (check after arithmetic)
- **B**: Saturating (`z = 100`, clamped)
- **C**: Wrapping (`z = 30`, wraps around)

**Recommendation**: Option A (panic) as default, provide `saturating()` and `wrapping()` functions later.

**Add to Phase 1A**: Define overflow behavior in documentation.

---

### Gap 5: Struct Padding Control 📋 MEDIUM PRIORITY

**Needed for wire formats**:
```runa
# Use case: Network protocol (no padding)
Type called "TcpHeader" with no padding:
    src_port as Integer16
    dst_port as Integer16
End Type

# Use case: Cache-line aligned
Type called "CacheLine" aligned to 64 bytes:
    data as Integer
End Type
```

**Add to Phase 2 (v0.0.8.7)**: Struct packing and alignment attributes.

---

### Gap 6: Endianness Handling 📋 MEDIUM PRIORITY

**Needed for network protocols**:
```runa
# Option A: Conversion functions
Process called "to_network_order_16" takes value as Integer16 returns Integer16

# Option B: Endian-aware types
Type called "Packet":
    id as Integer16 in network order
End Type
```

**Add to Phase 2 (v0.0.8.7)**: Endianness support.

---

### Gap 7: Float NaN/Infinity Handling 📋 MEDIUM PRIORITY

**Needed for IEEE 754 correctness**:
```runa
Let x as Float be 1.0 divided by 0.0    # Infinity
Let n as Float be 0.0 divided by 0.0    # NaN

# Need helper functions:
Process called "is_nan" takes x as Float returns Integer
Process called "is_infinity" takes x as Float returns Integer
Process called "is_finite" takes x as Float returns Integer
```

**Add to Phase 1B (v0.0.8.6)**: Float edge case functions.

---

### Gap 8: Bounds Check Optimization 🚀 PERFORMANCE

**Current plan**: Always insert runtime checks.

**Need**: Eliminate unnecessary checks:
```runa
Let x as Integer range 0 to 100 be 50    # No check needed (literal)
Set x to 50                              # No check needed (literal)
Set x to y                               # Check needed (unknown)
```

**Optimization passes**:
1. Eliminate checks on literals
2. Eliminate checks on already-checked values
3. Hoist checks out of loops

**Add to Phase 4 (v0.0.9)**: Bounds check optimization pass.

---

### Gap 9: Semantic Types (Newtype Pattern) 🎯 NICE TO HAVE

**Enables domain modeling**:
```runa
Type called "UserId" wrapping Integer
Type called "ProductId" wrapping Integer

Let user as UserId be UserId.wrap(123)
Let product as ProductId be ProductId.wrap(456)

Set user to product    # Compiler ERROR: type mismatch
```

**Add to v0.1.0+**: Newtype pattern for type safety.

---

### Gap 10: Range Inference in Expressions 🧠 ADVANCED FEATURE

**Current**: Arithmetic promotes to full Integer.

**Future**: Infer ranges through expressions:
```runa
Let a as Integer range 0 to 100
Let b as Integer range 0 to 50
Let c be a plus b    # Inferred: Integer range 0 to 150
Let d be a minus b   # Inferred: Integer range -50 to 100
```

**Add to v0.1.0+**: Range inference in type system.

---

## 📊 Gap Priority Summary

| Gap | Priority | Phase | Impact if Missing |
|-----|----------|-------|-------------------|
| 1. Signed/Unsigned Size | ⚠️ CRITICAL | 1A | Wrong sizes, corruption |
| 2. Arithmetic Promotion | ⚠️ HIGH | 1A | Ambiguous semantics |
| 3. Compile-Time Checks | ⚠️ HIGH | 1A | Preventable runtime errors |
| 4. Overflow Behavior | 🔄 HIGH | 1A | Undefined behavior |
| 5. Struct Padding | 📋 MEDIUM | 2 | Wire formats broken |
| 6. Endianness | 📋 MEDIUM | 2 | Network protocols broken |
| 7. Float NaN/Infinity | 📋 MEDIUM | 1B | IEEE 754 non-compliant |
| 8. Optimization | 🚀 MEDIUM | 4 | 10-20% slowdown |
| 9. Semantic Types | 🎯 LOW | Future | Weaker type safety |
| 10. Range Inference | 🧠 LOW | Future | More verbose code |

---

## 🎯 Integration with Existing Roadmap

### Updated Milestone Timeline:

| Version | Focus Area | Advanced Type System Work |
|---------|-----------|---------------------------|
| **v0.0.8.1** | Struct Construction ✅ | N/A (foundation complete) |
| **v0.0.8.2** | Collections + For Each | Uses ranges for optimized indexes |
| **v0.0.8.3** | Pattern Matching + ADTs | Pattern matching on ranged types |
| **v0.0.8.4** | Lambda + Type Inference | Infer ranges from literals |
| **v0.0.8.5** | String Interpolation | N/A |
| **v0.0.8.6** | **Advanced Types Phase 1** | **Range Constraints + Float/Float64** ⭐ |
| **v0.0.8.7** | **Advanced Types Phase 2** | **Integer16/32, Wire Format Types** ⭐ |
| **v0.0.9** | Error Handling + Generics | **FFI Types (CInt/CLong/CSize) + Warnings** ⭐ |
| **v0.1.0** | Beta Release | All advanced types complete ✅ |

### Why This Order:

1. **v0.0.8.6 (Range + Float)**: Foundation work, doesn't break anything
   - Ranges optimize existing Integer usage
   - Float enables HPC use cases
   - Both are additive (no breaking changes)

2. **v0.0.8.7 (Wire Format Types)**: Build on ranges
   - Explicit Integer16/32 complement automatic ranges
   - Needed before v0.1.0 (stdlib will use network protocols)

3. **v0.0.9 (FFI + Warnings)**: Integrate with Error Handling work
   - FFI types need Result/Option types for safe C interop
   - Warnings require type system maturity
   - Completes type system before v0.1.0

---

## 📊 Advantages Maintained (Verification)

### 1. Correctness Over Performance ✅ **ENHANCED**
- **Before**: Integer = 64-bit, no overflow
- **After**: Integer = 64-bit + bounds checks on ranges
- **Result**: MORE correct (catches out-of-range values)

### 2. Predictable Across Platforms ✅ **MAINTAINED**
- **Default Integer**: Always 8 bytes
- **Ranges**: Deterministic optimization (same everywhere)
- **FFI types**: Explicitly platform-specific (marked as such)
- **Result**: Same predictability, more explicit

### 3. Self-Documenting Memory Usage ✅ **ENHANCED**
```runa
Let age as Integer range 0 to 150      # Clearly 0-150, optimized to 1 byte
Let port as Integer16                  # Clearly 2 bytes, wire format
```
- **Result**: MORE self-documenting

### 4. Simpler Mental Model ⚠️ **SLIGHTLY MORE COMPLEX**
- **Complexity Added**: 4 levels (Integer → Range → Integer16/32 → FFI)
- **Still Simpler Than**:
  - C: int/short/long/long long/size_t/ssize_t/ptrdiff_t
  - Rust: i8/i16/i32/i64/i128/isize/u8/u16/u32/u64/u128/usize
- **Result**: Slight complexity, but BOUNDED and opt-in

### 5. Future-Proof ✅ **MAINTAINED**
- **Default Integer**: Still 8 bytes (future-proof)
- **FFI types**: Explicitly NOT future-proof (marked)
- **Result**: Same future-proofing

### 6. Natural Language Clarity ✅ **MAINTAINED**
```runa
Let age as Integer range 0 to 150      # Reads naturally
Let c_errno as CInt                    # "C integer" is clear
```
- **Result**: Same or better clarity

---

## 🎨 Philosophy Alignment: "Better Than All"

### vs Rust (Safety) ✅
- **Rust**: Must choose u8/u16/u32 upfront, limited bounds checking
- **Runa**: Automatic optimization + runtime bounds checks
- **Winner**: Runa (safer AND simpler)

### vs Python (Simplicity) ✅
- **Python**: One `int` type, no optimization
- **Runa**: Default Integer (simple), opt-in ranges (optimized)
- **Winner**: Runa (simple AND fast)

### vs C (Speed) ✅
- **C**: `int` varies, no bounds checks, manual optimization
- **Runa**: Automatic optimization (ranges), explicit types when needed
- **Winner**: Runa (fast AND safe)

### vs Go (Pragmatism) ✅
- **Go**: int/int8/int16/int32/int64, no automatic optimization
- **Runa**: Automatic optimization + explicit when needed
- **Winner**: Runa (less manual work, same performance)

---

## 📝 Syntax Quick Reference

### Progressive Disclosure (4 Levels):

#### Level 1: Beginner (Just use Integer)
```runa
Let count as Integer be 0
```
- Simple, safe, works everywhere
- 8 bytes (never overflows)

#### Level 2: Intermediate (Add ranges for optimization)
```runa
Let age as Integer range 0 to 150
Let temperature as Integer range -200 to 200
```
- Automatic optimization (1-4 bytes)
- Bounds checked at runtime
- Self-documenting constraints

#### Level 3: Advanced (Explicit wire format types)
```runa
Type called "TcpPacket":
    src_port as Integer16
    dst_port as Integer16
    sequence as Integer32
End Type
```
- Stable binary format
- No accidental changes
- Zero-copy serialization

#### Level 4: Expert (FFI types)
```runa
Process called "call_c_lib" calling C library takes fd as CInt returns CLong:
    # ...
End Process
```
- Platform-specific (explicit)
- Type-safe C interop
- Requires explicit conversion

---

## 🧪 Test Coverage

### Unit Tests (per phase):
1. **Range constraints**: 20+ tests
   - Basic ranges (positive, negative, zero)
   - Struct fields with ranges
   - Bounds violations
   - Size computation

2. **Float types**: 15+ tests
   - Arithmetic operations
   - Comparisons
   - Conversion (Integer ↔ Float)
   - Struct fields

3. **Wire format types**: 10+ tests
   - Fixed size verification
   - Binary serialization
   - Network protocols

4. **FFI types**: 15+ tests
   - C function calls
   - Type conversions
   - Platform-specific behavior

### Integration Tests:
1. **Embedded system simulation** (range optimization)
2. **HPC particle simulation** (Float performance)
3. **Network protocol parser** (Integer16/32 wire formats)
4. **C library wrapper** (FFI types)

### Performance Benchmarks:
- Compare range-optimized vs C equivalents
- Compare Float vs C float performance
- Measure bounds check overhead (should be <5%)

---

## 📦 Deliverables

### v0.0.8.6:
- ✅ Range-constrained integers working
- ✅ Float and Float64 types working
- ✅ 35+ tests passing
- ✅ Documentation updated
- ✅ Example: embedded sensor struct (optimized)
- ✅ Example: HPC particle simulation (matches C performance)

### v0.0.8.7:
- ✅ Integer16/Integer32/UInteger16/UInteger32 working
- ✅ Wire format stability guarantees
- ✅ 10+ tests passing
- ✅ Example: TCP packet parser

### v0.0.9:
- ✅ CInt/CLong/CSize/CChar working
- ✅ FFI boundary safety checks
- ✅ Smart compiler warnings
- ✅ 15+ tests passing
- ✅ Example: POSIX file I/O wrapper

---

## 🎯 Success Metrics

### Technical Metrics:
1. **Memory Efficiency**: Range-optimized structs use 40-60% less memory than default
2. **Performance**: Float operations match C (within 5%)
3. **Safety**: 100% of range violations caught at runtime
4. **Compatibility**: FFI types correctly match C ABI on all platforms

### Philosophy Metrics (Better Than All):
1. **vs Rust**: ✅ Simpler syntax, automatic optimization, same safety
2. **vs Python**: ✅ Same simplicity (for beginners), 10-100x faster
3. **vs C**: ✅ Same speed, way safer, more expressive
4. **vs Go**: ✅ More automatic, less manual type juggling

### User Experience Metrics:
1. **Learning Curve**: Beginners only need to know Integer (Level 1)
2. **Progressive Disclosure**: Each level is opt-in, natural progression
3. **Error Messages**: Clear, actionable (e.g., "Use Integer16 for wire format")
4. **Documentation**: Examples for each level, clear use cases

---

## 📚 Documentation Plan

### New Documentation:
1. **Type System Guide** (`docs/TYPES.md`)
   - 4 levels of type usage
   - When to use each level
   - Examples for each use case

2. **Range Constraints Tutorial** (`docs/RANGES.md`)
   - How ranges work
   - Automatic optimization
   - Bounds checking behavior

3. **FFI Guide** (`docs/FFI.md`)
   - Calling C libraries
   - Type conversion rules
   - Platform differences

4. **Wire Format Best Practices** (`docs/WIRE_FORMATS.md`)
   - When to use Integer16/32
   - Binary serialization
   - Stability guarantees

### Updated Documentation:
1. **Language Reference** - Add new type syntax
2. **Tutorial** - Show range examples in early chapters
3. **Stdlib Docs** - Use ranges in stdlib examples

---

## 🚀 Migration Path (For Future Users)

### Existing Code (v0.0.8.5 and earlier):
```runa
Let x as Integer be 10
```
- **Still works!** No breaking changes.

### Opt-In Optimization (v0.0.8.6+):
```runa
Let x as Integer range 0 to 100 be 10
```
- **Better**: Optimized to 1 byte, bounds checked

### Wire Format Migration (v0.0.8.7+):
```runa
# Before (risky):
Type called "Packet":
    id as Integer range 0 to 65535

# After (stable):
Type called "Packet":
    id as Integer16  # Locked at 2 bytes
```
- **Safer**: Compiler warns if range changes

---

## 🎓 Teaching Plan (Progressive Disclosure)

### Week 1 (Beginners):
- Just use `Integer` (8 bytes)
- Simple, safe, works

### Week 2-3 (Intermediate):
- Learn ranges: `Integer range 0 to 100`
- Optimization happens automatically
- Understand bounds checking

### Week 4-5 (Advanced):
- Learn wire format types: `Integer16`, `Integer32`
- Understand stability guarantees
- Binary serialization

### Week 6+ (Expert):
- Learn FFI types: `CInt`, `CLong`, `CSize`
- Calling C libraries safely
- Platform differences

**Result**: Natural learning curve, each level builds on previous.

---

## ✅ Checklist for Implementation

### Phase 1A (Range Constraints):
- [ ] **FIX STACK OFFSETS** (CRITICAL - must do first!)
  - [ ] Add size/alignment/signedness fields to Variable struct
  - [ ] Implement `compute_stack_layout()` in codegen
  - [ ] Replace ALL `multiplied by 8` with actual offsets
  - [ ] Implement `codegen_load_variable()` with sign-extension (movsbq/movswq/movslq)
  - [ ] Implement `codegen_store_variable()` with size-specific instructions
  - [ ] Test with `test_stack_layout.runa` (mixed sizes)
- [ ] Add range syntax to parser
- [ ] **Gap 1**: Implement CORRECT `compute_range_size()` (signed vs unsigned)
- [ ] **Gap 1**: Implement `compute_range_signedness()` (track if range has negatives)
- [ ] **Gap 2**: Define arithmetic promotion rules (promote to Integer)
- [ ] **Gap 3**: Implement compile-time literal range verification
- [ ] **Gap 4**: Define overflow behavior (panic by default)
- [ ] Generate bounds checks in codegen
- [ ] Add runtime error handler (`bounds_check_failed()`)
- [ ] Write 20+ tests (including stack layout, signed ranges, overflow)
- [ ] Update documentation

### Phase 1B (Float Types):
- [ ] Add Float/Float64 keywords
- [ ] Parse float literals
- [ ] Generate SSE/AVX instructions
- [ ] **Gap 7**: Add NaN/Infinity helper functions (is_nan, is_infinity, is_finite)
- [ ] Add float runtime functions
- [ ] Write 15+ tests (including NaN/Infinity edge cases)
- [ ] Benchmark vs C

### Phase 2 (Wire Format Types):
- [ ] Add Integer16/32/UInteger16/32 keywords
- [ ] Ensure fixed sizes
- [ ] **Gap 5**: Add struct padding control (`with no padding`, `aligned to N bytes`)
- [ ] **Gap 6**: Add endianness support (conversion functions or type annotations)
- [ ] Zero-copy serialization example
- [ ] Write 10+ tests (including padding and endianness)
- [ ] Document stability guarantees

### Phase 3 (FFI Types):
- [ ] Add CInt/CLong/CSize keywords
- [ ] Platform-specific sizes
- [ ] Explicit conversion enforcement
- [ ] Write 15+ tests
- [ ] Test on Linux + Windows

### Phase 4 (Warnings & Optimization):
- [ ] Pattern match type names
- [ ] Detect range changes
- [ ] Detect serialization
- [ ] **Gap 8**: Implement bounds check optimization (eliminate literal checks, hoist from loops)
- [ ] Helpful error messages
- [ ] Document best practices

### Future (v0.1.0+):
- [ ] **Gap 9**: Newtype pattern for semantic types
- [ ] **Gap 10**: Range inference through arithmetic expressions

---

## 🎉 End Result

**A type system that is:**
1. ✅ Simple by default (just use Integer)
2. ✅ Powerful when needed (ranges, explicit types, FFI)
3. ✅ Safer than Rust (automatic bounds checks)
4. ✅ Simpler than Rust (no u8/u16/u32/u64 maze)
5. ✅ Faster than Python (optimized storage)
6. ✅ As fast as C (when needed)
7. ✅ More correct than C (bounds checked)
8. ✅ Better than all (in their respective domains)

**Philosophy achieved**: "Better than all" through progressive disclosure and opt-in complexity.
