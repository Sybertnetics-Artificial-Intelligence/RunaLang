# Type System Design for v0.0.8.4.5.1

## Overview
Complete type system implementation including:
- Fixed-size integers (8/16/32/64/128-bit, signed and unsigned)
- Floating-point types (Float/Float64)
- Pointer type
- Refinement types with compile-time and runtime constraints
- Type conversions and casts
- Binary literals
- Endianness operations
- Escape analysis for automatic stack allocation

## Token Additions

### New Type Keywords
```
TOKEN_INTEGER8 = 188
TOKEN_INTEGER16 = 189
TOKEN_INTEGER32 = 190
TOKEN_INTEGER64 = 191
TOKEN_INTEGER128 = 192
TOKEN_UNSIGNED_INTEGER8 = 193
TOKEN_UNSIGNED_INTEGER16 = 194
TOKEN_UNSIGNED_INTEGER32 = 195
TOKEN_UNSIGNED_INTEGER64 = 196
TOKEN_UNSIGNED_INTEGER128 = 197
TOKEN_FLOAT = 198
TOKEN_FLOAT64 = 199
```

### Existing Tokens to Use
- `TOKEN_AS` (34) - already exists for type annotations
- `TOKEN_TYPE` (50) - already exists for type definitions
- `TOKEN_WHERE` (153) - already exists for refinement constraints
- `TOKEN_POINTER` (124) - already exists for pointer type

## Syntax

### Type Inference (Default - Recommended)
```runa
Let x be 100                     # Infers Integer32 (default for integer literals)
Let y be 1000000000000           # Infers Integer64 (too large for Integer32)
Let pi be 3.14159                # Infers Float64 (default for float literals)
Let ptr be allocate(64)          # Infers Pointer (from function return type)
Let flags be 0b10110101          # Infers Integer32 from binary literal
```

### Explicit Type Casts (Optional - When Control Needed)
```runa
Let byte be 127 as Integer8                    # Explicit cast to 8-bit
Let unsigned_byte be 255 as UnsignedInteger8   # Explicit unsigned
Let float_pi be 3.14159 as Float               # Explicit 32-bit float
Let ptr be some_value as Pointer               # Explicit pointer type
```

**When to use explicit casts:**
- Specific size requirements (Integer8 vs Integer32 for memory efficiency)
- Binary protocols/FFI requiring exact types
- Disambiguating signed vs unsigned
- Performance optimization (smaller types = less memory)

### Refinement Types
```runa
Type called "Percentage" is Integer32 where value is greater than or equal to 0 and value is less than or equal to 100
Type called "Port" is Integer32 where value is greater than 0 and value is less than 65536
Type called "PositiveInteger" is Integer64 where value is greater than 0
Type called "ValidAge" is Integer32 where value is greater than or equal to 0 and value is less than 150
```

### Type Conversions (Cast Syntax)
```runa
Let x be 1000
Let y be x as Integer64                        # Sign-extend 32→64
Let z be 255 as UnsignedInteger8
Let overflow be z as Integer8                  # Truncate/reinterpret (warning)
```

### Binary Literals
```runa
Let flags be 0b10110101                        # Infers Integer32
Let mask be 0b1111000011110000 as Integer16    # Explicit 16-bit
Let hex be 0x1F3A                              # Infers Integer32
```

### Floating-Point Literals
```runa
Let a be 3.14          # Infers Float64
Let b be 2.5e10        # Scientific notation: 2.5 × 10^10
Let c be 1.0e-5        # 0.00001
Let d be 3.14 as Float # Explicit Float (32-bit)
```

## AST Changes

### Type Node Structure
```
Type Node:
  - kind: Integer (0=Integer8, 1=Integer16, 2=Integer32, 3=Integer64, 4=Integer128,
                   5=UnsignedInteger8, 6=UnsignedInteger16, 7=UnsignedInteger32,
                   8=UnsignedInteger64, 9=UnsignedInteger128,
                   10=Float, 11=Float64, 12=Pointer)
  - refinement_constraint: Pointer (nullable - AST expression for constraint)
  - name: String (for named refinement types)
```

### Variable Declaration with Type
```
Let Statement:
  - name: String
  - type: Type Node (nullable - inferred if not provided)
  - value: Expression
```

### Function Parameter with Type
```
Parameter:
  - name: String
  - type: Type Node
```

### Cast Expression
```
Cast Expression:
  - expression: Expression
  - target_type: Type Node
```

## Lexer Changes

### Integer Literal Classification
Current lexer creates TOKEN_INTEGER for all numeric literals.
Need to:
1. Detect floating-point (contains '.' or 'e'/'E')
2. Parse binary literals (0b prefix)
3. Store literal type in token metadata

### Float Literal Structure
```
Token for Float:
  - type: TOKEN_FLOAT_LITERAL (new)
  - float_value: stored as 64-bit double
  - precision: 0=inferred, 1=Float, 2=Float64
```

### Binary Literal Parsing
```
If starts with "0b" or "0B":
  - Parse binary digits (0-1 only)
  - Convert to integer value
  - Store as TOKEN_INTEGER
```

## Type Checking

### Type Inference Rules
1. Integer literals → Integer32 by default
2. Float literals → Float64 by default
3. Binary operations preserve larger type
4. Comparisons work across compatible types
5. Explicit cast required for narrowing conversions

### Refinement Type Checking
**Compile-time (constants):**
```runa
Let percent as Percentage be 50      # OK - verified at parse time
Let invalid as Percentage be 150     # ERROR - caught by type checker
```

**Runtime (dynamic values):**
```runa
Process called "set_volume" takes vol as Percentage returns Nothing:
    # Compiler inserts at entry:
    # check_range(vol, 0, 100, "Percentage")
    Note: Function body
End Process
```

## Codegen

### Integer Size Instructions
```
Integer8:     movb (load), movsbq (sign-extend), movzbq (zero-extend)
Integer16:    movw (load), movswq (sign-extend), movzwq (zero-extend)
Integer32:    movl (load), movslq (sign-extend), movzlq (zero-extend)
Integer64:    movq (load)
Integer128:   movdqa (SSE load), paddq/psubq (arithmetic)
```

### Unsigned vs Signed Comparisons
```
Signed:       jl, jle, jg, jge (signed comparisons)
Unsigned:     jb, jbe, ja, jae (unsigned comparisons)
```

### Floating-Point Instructions
```
Float (32-bit):
  - movss      (move scalar single)
  - addss/subss/mulss/divss (arithmetic)
  - ucomiss    (comparison)

Float64 (64-bit):
  - movsd      (move scalar double)
  - addsd/subsd/mulsd/divsd (arithmetic)
  - ucomisd    (comparison)
```

### 128-bit Integer Operations
```
Load/Store:   movdqa %xmm0, (%rax)
Addition:     paddq %xmm1, %xmm0  (add two 64-bit integers in parallel)
Subtraction:  psubq %xmm1, %xmm0
Bitwise:      pand/por/pxor
```

### Endianness Operations
```
Process called "to_big_endian32" takes value as Integer32 returns Integer32:
    Inline Assembly:
        movl %value, %eax
        bswap %eax
        movl %eax, %result
    End Assembly
End Process
```

## Runtime Functions

### Constraint Checking
```runa
Process called "check_range_i32" takes value as Integer32, min as Integer32, max as Integer32, type_name as Pointer returns Nothing:
    If value is less than min or value is greater than max:
        Display "Range constraint violation for ", type_name
        Display ": expected ", integer_to_string(min as Integer64)
        Display " to ", integer_to_string(max as Integer64)
        Display ", got ", integer_to_string(value as Integer64)
        exit_with_code(1)
    End If
End Process
```

### Floating-Point Math
```runa
Process called "sqrt_f64" takes x as Float64 returns Float64
Process called "pow_f64" takes x as Float64, y as Float64 returns Float64
Process called "sin_f64" takes x as Float64 returns Float64
Process called "cos_f64" takes x as Float64 returns Float64
Process called "floor_f64" takes x as Float64 returns Float64
Process called "ceil_f64" takes x as Float64 returns Float64
```
Initially implemented as FFI calls to libm, later pure Runa.

### Binary I/O
```runa
Process called "read_i32" takes fd as Integer32 returns Integer32
Process called "write_i32" takes fd as Integer32, value as Integer32 returns Integer32
Process called "read_bytes" takes fd as Integer32, buffer as Pointer, count as Integer64 returns Integer64
Process called "write_bytes" takes fd as Integer32, buffer as Pointer, count as Integer64 returns Integer64
```

### Endianness Helpers
```runa
Process called "htobe16" takes value as Integer16 returns Integer16  # Host to big-endian
Process called "htobe32" takes value as Integer32 returns Integer32
Process called "htobe64" takes value as Integer64 returns Integer64
Process called "be16toh" takes value as Integer16 returns Integer16  # Big-endian to host
Process called "le16toh" takes value as Integer16 returns Integer16
```

## Escape Analysis (Optimization)

### Goal
Automatically determine if allocations can go on stack instead of heap.

### Analysis
```runa
Process called "example" takes size as Integer32 returns Nothing:
    Let arr be allocate(size times 8)  # Analyze: does 'arr' escape?
    # ... use arr locally ...
    # No return of arr, no storing to global, no passing to escaping function
    # → Stack allocate arr, no deallocate needed
End Process
```

### Implementation Steps
1. Build escape graph for all allocations
2. Track if pointer:
   - Returned from function
   - Stored in heap-allocated structure
   - Passed to function that causes escape
3. If doesn't escape → replace `allocate()` with stack allocation
4. Remove corresponding `deallocate()` calls

## Implementation Order

### Phase 1: Lexer
1. Add new type keyword tokens (Integer8/16/32/64/128, UnsignedInteger*, Float/Float64)
2. Add binary literal parsing (0b prefix)
3. Add floating-point literal parsing (detect '.' or 'e')
4. Store literal type metadata in tokens

### Phase 2: Parser
1. Parse cast expressions: `value as TargetType` (for explicit type control)
2. Parse refinement type definitions: `Type called "X" is Base where constraint`
3. **NO type annotations in Let statements** - pure inference by default
4. Add type fields to AST nodes for inferred/cast types

### Phase 3: Type Checker
1. Build type inference engine
2. Implement compile-time constraint checking (constants)
3. Generate runtime constraint checks (dynamic values)
4. Validate type conversions (warn on narrowing)

### Phase 4: Codegen
1. Size-specific instructions (movb/w/l/q)
2. Sign/zero extension (movsbq, movzbq, etc.)
3. Signed vs unsigned comparisons (jl vs jb)
4. Floating-point SSE instructions (movss/movsd, addss/addsd)
5. 128-bit SSE instructions (movdqa, paddq, psubq)
6. Endianness operations (bswap)

### Phase 5: Runtime
1. Constraint checking helpers
2. Floating-point math (FFI to libm)
3. Binary I/O functions
4. Endianness conversion helpers

### Phase 6: Optimization
1. Implement escape analysis
2. Replace non-escaping allocations with stack alloc
3. Remove unnecessary deallocations

## Testing Strategy

### Unit Tests
1. Each integer size (8/16/32/64/128)
2. Unsigned integer operations
3. Floating-point arithmetic
4. Type conversions (sign-extend, zero-extend, truncate)
5. Refinement type compile-time checks
6. Refinement type runtime checks
7. Binary literals
8. Endianness operations

### Integration Tests
1. Mixed-type expressions
2. Function calls with typed parameters
3. Refinement types in real scenarios (Port, Percentage)
4. Stack allocation optimization

### Bootstrap Test
1. Compile v0.0.8.4.5.1 with v0.0.8.4.5
2. Verify all type features work
3. Recompile v0.0.8.4.5.1 with itself (self-hosting check)

## Migration Notes

### Backward Compatibility
- Existing code without type annotations continues to work
- Default types: Integer → Integer32, literals → Integer32/Float64
- Explicit Pointer type distinguishes from Integer (fixes arena bug!)

### Breaking Changes
- `allocate()` now returns `Pointer` not `Integer64`
- Math functions use specific Float/Float64 types
- Binary I/O requires explicit Integer8/16/32/64 types
