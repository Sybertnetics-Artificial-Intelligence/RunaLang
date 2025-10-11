# v0.0.8.5 Primitive Implementation Plan
## Complete Dependency-Ordered Build Sequence

**Goal:** Implement all primitives from codegen.runa into modular, properly-structured files with NO C dependencies.

## Phase 0: Foundation - Pure Assembly & Syscalls (NO dependencies)

These are the absolute foundation - they depend on NOTHING.

### 0.1 `assembly/syscall.runa` - Direct OS System Calls
**Purpose:** Raw syscall interface to OS kernel (replaces C runtime)
**Functions needed:**
- `syscall_read(fd, buf, count)` - read syscall (syscall 0)
- `syscall_write(fd, buf, count)` - write syscall (syscall 1)
- `syscall_open(path, flags, mode)` - open syscall (syscall 2)
- `syscall_close(fd)` - close syscall (syscall 3)
- `syscall_mmap(addr, length, prot, flags, fd, offset)` - mmap syscall (syscall 9)
- `syscall_munmap(addr, length)` - munmap syscall (syscall 11)
- `syscall_brk(addr)` - brk syscall (syscall 12)
- `syscall_exit(code)` - exit syscall (syscall 60)

**Implementation:** Pure inline assembly using Linux x86_64 ABI
```runa
Process called "syscall_write" takes fd, buf, count returns Integer:
    Let result be 0
    Inline Assembly:
        "movq %rdi, %rax"      # syscall number (1 for write)
        "movq %rsi, %rdi"      # fd
        "movq %rdx, %rsi"      # buf
        "movq %rcx, %rdx"      # count
        "movq $1, %rax"        # SYS_write
        "syscall"
        "movq %rax, -8(%rbp)"  # store result
    End Assembly
    Return result
End Process
```

**Depends on:** NOTHING (this IS the foundation)

---

### 0.2 `assembly/register_map.runa` - CPU Register Constants
**Purpose:** Register definitions for inline assembly
**Constants:**
- Register names (RAX, RBX, RCX, etc.)
- Register sizes
- Calling convention register mappings

**Depends on:** NOTHING

---

### 0.3 `core/memory_core.runa` - Raw Memory Operations
**Purpose:** Memory read/write using inline assembly (replaces C runtime memory functions)
**Functions:**
- `memory_read_byte(addr) -> byte`
- `memory_write_byte(addr, value)`
- `memory_read_int32(addr) -> int`
- `memory_write_int32(addr, value)`
- `memory_read_int64(addr) -> int`
- `memory_write_int64(addr, value)`
- `memory_copy(dest, src, length)` - replaces memcpy
- `memory_set(dest, value, length)` - replaces memset
- `memory_compare(a, b, length)` - replaces memcmp

**Implementation:** Inline assembly with rep movsb/stosb
**Depends on:** NOTHING (pure assembly)

---

### 0.4 `core/pointer_primitive.runa` - Pointer Arithmetic
**Purpose:** Pointer manipulation
**Functions:**
- `pointer_add(ptr, offset) -> ptr`
- `pointer_subtract(ptr, offset) -> ptr`
- `pointer_difference(ptr1, ptr2) -> offset`
- `pointer_is_null(ptr) -> bool`

**Depends on:** NOTHING

---

## Phase 1: Memory Management (Depends on Phase 0)

### 1.1 `memory/layout.runa` - Memory Allocator & Variable Tracking
**Purpose:** Heap allocation, variable storage
**Functions from codegen:**
- `allocate(size)` - heap allocation using syscall_brk/mmap
- `deallocate(ptr)` - heap deallocation
- `find_variable(codegen, name)` - variable lookup
- `add_variable(codegen, name)` - add variable to symbol table
- `add_variable_with_type(codegen, name, type_name)`
- `add_variable_with_type_and_param_flag(codegen, name, type_name, is_param)`
- `calculate_stack_offset()`

**Depends on:**
- `syscall.runa` (for brk/mmap)
- `memory_core.runa` (for memory operations)

---

### 1.2 `core/alignment_core.runa` - Memory Alignment
**Purpose:** Alignment calculations
**Functions:**
- `align_up(size, alignment) -> size`
- `align_down(size, alignment) -> size`
- `is_aligned(ptr, alignment) -> bool`

**Depends on:**
- `pointer_primitive.runa`

---

### 1.3 `intrinsics/sizeof.runa` - Size Calculations
**Purpose:** Calculate type sizes
**Functions:**
- `calculate_type_size(type_name) -> size`

**Depends on:**
- `alignment_core.runa`

---

### 1.4 `intrinsics/offsetof.runa` - Field Offset Calculations
**Purpose:** Struct field offsets
**Functions:**
- `calculate_field_offset(struct_type, field_name) -> offset`

**Depends on:**
- `sizeof.runa`
- `alignment_core.runa`

---

### 1.5 `intrinsics/alignof.runa` - Alignment Requirements
**Purpose:** Type alignment requirements
**Functions:**
- `get_type_alignment(type_name) -> alignment`

**Depends on:** NOTHING (returns constants)

---

## Phase 2: Core Primitives (Depends on Phases 0-1)

### 2.1 `core/string_primitive.runa` - String Operations
**Purpose:** String handling and literals
**Functions from codegen:**
- `add_string_literal(codegen, value)` - add to string table
- `string_length(str) -> length`
- `string_concat(str1, str2) -> new_string`
- `string_equals(str1, str2) -> bool`
- `string_duplicate(str) -> new_string`

**Depends on:**
- `memory_core.runa` (memory_copy, memory_compare)
- `memory/layout.runa` (allocate/deallocate)

---

### 2.2 `core/arithmetic_core.runa` - Arithmetic Primitives
**Purpose:** Basic arithmetic operations
**Functions:**
- `add(a, b) -> result`
- `subtract(a, b) -> result`
- `multiply(a, b) -> result`
- `divide(a, b) -> result`
- `modulo(a, b) -> result`

**Depends on:** NOTHING (inline assembly or basic ops)

---

### 2.3 `core/comparison_core.runa` - Comparison Primitives
**Purpose:** Comparison operations
**Functions:**
- `equals(a, b) -> bool`
- `not_equals(a, b) -> bool`
- `less_than(a, b) -> bool`
- `greater_than(a, b) -> bool`
- `less_or_equal(a, b) -> bool`
- `greater_or_equal(a, b) -> bool`

**Depends on:** NOTHING

---

### 2.4 `core/bitwise_core.runa` - Bitwise Operations
**Purpose:** Bitwise primitives
**Functions:**
- `bitwise_and(a, b) -> result`
- `bitwise_or(a, b) -> result`
- `bitwise_xor(a, b) -> result`
- `bitwise_not(a) -> result`
- `left_shift(a, count) -> result`
- `right_shift(a, count) -> result`

**Depends on:** NOTHING

---

### 2.5 `core/logical_core.runa` - Logical Operations
**Purpose:** Boolean logic
**Functions:**
- `logical_and(a, b) -> bool`
- `logical_or(a, b) -> bool`
- `logical_not(a) -> bool`

**Depends on:** NOTHING

---

### 2.6 `core/boolean_primitive.runa` - Boolean Type
**Purpose:** Boolean true/false
**Constants:**
- `TRUE = 1`
- `FALSE = 0`

**Depends on:** NOTHING

---

### 2.7 `core/void_primitive.runa` - Void Type
**Purpose:** Void type representation
**Functions:**
- `is_void_type(type) -> bool`

**Depends on:** NOTHING

---

## Phase 3: Type System (Depends on Phases 0-2)

### 3.1 `types/validation.runa` - Type Validation
**Purpose:** Type checking and validation
**Functions from codegen:**
- `get_expression_type(codegen, expr) -> type_name`
- `validate_type(type_name) -> bool`
- `types_compatible(type1, type2) -> bool`

**Depends on:**
- `sizeof.runa`
- `string_primitive.runa`

---

### 3.2 `types/access.runa` - Field Access
**Purpose:** Struct/type field access
**Functions from codegen:**
- `generate_field_access(codegen, expr)` - codegen for field access
- `get_field_type(struct_type, field_name) -> type`

**Depends on:**
- `offsetof.runa`
- `types/validation.runa`

---

### 3.3 `types/construction.runa` - Type Construction
**Purpose:** Create type instances
**Functions:**
- `construct_struct(type_name, fields) -> instance`
- `construct_array(element_type, size) -> array`

**Depends on:**
- `memory/layout.runa`
- `sizeof.runa`

---

### 3.4 `types/conversion.runa` - Type Conversions
**Purpose:** Type casting and conversions
**Functions:**
- `cast_to_type(value, from_type, to_type) -> converted_value`

**Depends on:**
- `types/validation.runa`

---

### 3.5 `types/compiler_internals.runa` - Compiler Type Internals
**Purpose:** Internal type representations
**Functions:**
- `create_type_descriptor(type_name) -> descriptor`

**Depends on:**
- `memory/layout.runa`

---

## Phase 4: Operators (Depends on Phases 0-3)

### 4.1 `operators/arithmetics.runa` - Arithmetic Code Generation
**Purpose:** Generate code for arithmetic expressions
**Functions from codegen:**
- `generate_binary_op(codegen, expr)` - +, -, *, /, %

**Depends on:**
- `arithmetic_core.runa`
- `types/validation.runa`
- `assembly/machine_code.runa` (emit functions)

---

### 4.2 `operators/comparison.runa` - Comparison Code Generation
**Purpose:** Generate code for comparisons
**Functions from codegen:**
- `generate_comparison(codegen, expr)` - ==, !=, <, >, <=, >=

**Depends on:**
- `comparison_core.runa`
- `types/validation.runa`

---

### 4.3 `operators/logical.runa` - Logical Code Generation
**Purpose:** Generate code for logical operations
**Functions from codegen:**
- `generate_unary_op(codegen, expr)` - NOT, AND, OR

**Depends on:**
- `logical_core.runa`

---

### 4.4 `operators/bitwise.runa` - Bitwise Code Generation
**Purpose:** Generate code for bitwise operations
**Functions:**
- `generate_bitwise_op(codegen, expr)` - &, |, ^, ~, <<, >>

**Depends on:**
- `bitwise_core.runa`

---

## Phase 5: Control Flow (Depends on Phases 0-4)

### 5.1 `control_flow/branch.runa` - Branch Instructions
**Purpose:** Conditional branching
**Functions:**
- `generate_conditional_branch(codegen, condition, label)`
- `generate_unconditional_branch(codegen, label)`

**Depends on:**
- `assembly/machine_code.runa`

---

### 5.2 `control_flow/jump.runa` - Jump Instructions
**Purpose:** Unconditional jumps
**Functions:**
- `generate_jump(codegen, label)`
- `generate_label(codegen, label_name)`

**Depends on:**
- `assembly/machine_code.runa`

---

### 5.3 `control_flow/return.runa` - Return Statements
**Purpose:** Function returns
**Functions:**
- `generate_return(codegen, expr)`

**Depends on:**
- `assembly/machine_code.runa`

---

### 5.4 `control_flow/call.runa` - Function Calls
**Purpose:** Function call code generation
**Functions from codegen:**
- `generate_function_call(codegen, expr)`
- `generate_indirect_call(codegen, expr)`

**Depends on:**
- `assembly/machine_code.runa`
- `types/validation.runa`

---

### 5.5 `control_flow/lambda.runa` - Lambda/Closure Support
**Purpose:** Lambda code generation
**Functions from codegen:**
- `generate_lambda(codegen, expr)`
- `generate_lambda_call(codegen, expr)`

**Depends on:**
- `control_flow/call.runa`
- `memory/layout.runa`

---

### 5.6 `control_flow/statements.runa` - Statement Generation
**Purpose:** Generate code for all statement types
**Functions from codegen:**
- `generate_statement(codegen, stmt)` - dispatcher
- `generate_if_statement(codegen, stmt)`
- `generate_while_statement(codegen, stmt)`
- `generate_for_statement(codegen, stmt)`
- `generate_break_statement(codegen, stmt)`
- `generate_continue_statement(codegen, stmt)`
- `generate_return_statement(codegen, stmt)`
- `generate_expression_statement(codegen, stmt)`

**Depends on:**
- `control_flow/branch.runa`
- `control_flow/jump.runa`
- `control_flow/return.runa`

---

## Phase 6: Variables (Depends on Phases 0-5)

### 6.1 `variables/statements.runa` - Variable Statements
**Purpose:** Let/Set statement code generation
**Functions from codegen:**
- `generate_let_statement(codegen, stmt)`
- `generate_set_statement(codegen, stmt)`

**Depends on:**
- `memory/layout.runa` (variable tracking)
- `types/validation.runa`

---

## Phase 7: Intrinsics (Depends on Phases 0-6)

### 7.1 `intrinsics/builtins.runa` - Built-in Functions
**Purpose:** Compiler built-ins
**Functions from codegen:**
- `generate_builtin_call(codegen, expr)`
  - print_string
  - print_integer
  - allocate
  - deallocate

**Depends on:**
- `syscall.runa` (for I/O)
- `memory/layout.runa`

---

## Phase 8: Assembly Generation (Depends on ALL above)

### 8.1 `assembly/machine_code.runa` - Main Code Generator
**Purpose:** Orchestrate all code generation
**Functions from codegen:**
- `emit_line(output_file, line)` - write assembly line
- `generate_expression(codegen, expr)` - dispatcher for expressions
- `generate_function(codegen, func)` - generate function code
- `generate_program(codegen, program)` - generate entire program
- `create_codegen(output_file) -> codegen`
- `destroy_codegen(codegen)`

**Imports ALL primitives above**

**Depends on:**
- Everything (this is the orchestrator)

---

### 8.2 `assembly/inline_asm.runa` - Inline Assembly
**Purpose:** Handle inline assembly blocks
**Functions:**
- `generate_inline_asm(codegen, asm_block)`

**Depends on:**
- `assembly/machine_code.runa`

---

## Phase 9: I/O (Depends on syscalls)

### 9.1 `io/statements.runa` - I/O Statement Generation
**Purpose:** Print/Display statements
**Functions:**
- `generate_print_statement(codegen, stmt)`
- `generate_display_statement(codegen, stmt)`

**Depends on:**
- `syscall.runa` (syscall_write)
- `string_primitive.runa`

---

## Phase 10: Collections & Constants (Optional Enhancements)

### 10.1 `collections/literals.runa` - Collection Literals
**Purpose:** Array/list literal syntax
**Functions:**
- `generate_array_literal(codegen, expr)`
- `generate_list_literal(codegen, expr)`

**Depends on:**
- `memory/layout.runa`
- `types/construction.runa`

---

### 10.2 `constants/constants.runa` - Compile-Time Constants
**Purpose:** Constant folding
**Functions:**
- `evaluate_constant_expression(expr) -> value`

**Depends on:**
- `arithmetic_core.runa`
- `comparison_core.runa`

---

### 10.3 `constants/literal.runa` - Literal Values
**Purpose:** Literal parsing
**Functions:**
- `parse_integer_literal(str) -> value`
- `parse_string_literal(str) -> value`

**Depends on:**
- `string_primitive.runa`

---

### 10.4 `constants/null.runa` - Null Pointer
**Purpose:** Null pointer constant
**Constant:**
- `NULL = 0`

**Depends on:** NOTHING

---

## Phase 11: Pattern Matching (Advanced)

### 11.1 `pattern/matching.runa` - Pattern Matching
**Purpose:** Match statement code generation
**Functions:**
- `generate_match_statement(codegen, stmt)`

**Depends on:**
- `control_flow/branch.runa`
- `types/validation.runa`

---

## Build Order Summary

**Layer 0 (Foundation):**
1. assembly/syscall.runa
2. assembly/register_map.runa
3. core/memory_core.runa
4. core/pointer_primitive.runa

**Layer 1 (Memory):**
5. memory/layout.runa
6. core/alignment_core.runa
7. intrinsics/sizeof.runa
8. intrinsics/offsetof.runa
9. intrinsics/alignof.runa

**Layer 2 (Core Primitives):**
10. core/string_primitive.runa
11. core/arithmetic_core.runa
12. core/comparison_core.runa
13. core/bitwise_core.runa
14. core/logical_core.runa
15. core/boolean_primitive.runa
16. core/void_primitive.runa

**Layer 3 (Type System):**
17. types/validation.runa
18. types/access.runa
19. types/construction.runa
20. types/conversion.runa
21. types/compiler_internals.runa

**Layer 4 (Operators):**
22. operators/arithmetics.runa
23. operators/comparison.runa
24. operators/logical.runa
25. operators/bitwise.runa

**Layer 5 (Control Flow):**
26. control_flow/branch.runa
27. control_flow/jump.runa
28. control_flow/return.runa
29. control_flow/call.runa
30. control_flow/lambda.runa
31. control_flow/statements.runa

**Layer 6 (Variables):**
32. variables/statements.runa

**Layer 7 (Intrinsics):**
33. intrinsics/builtins.runa

**Layer 8 (Assembly):**
34. assembly/machine_code.runa (imports ALL above)
35. assembly/inline_asm.runa

**Layer 9 (I/O):**
36. io/statements.runa

**Layer 10 (Optional):**
37. collections/literals.runa
38. constants/constants.runa
39. constants/literal.runa
40. constants/null.runa

**Layer 11 (Advanced):**
41. pattern/matching.runa

---

## Implementation Strategy

1. **Start with Layer 0** - syscalls and memory primitives
2. **Test each primitive independently** with v0.0.8.4.5 compiler
3. **Build layer by layer** - never skip dependencies
4. **machine_code.runa imports everything** at the end
5. **Test compilation** after each layer is complete

This gives us a **complete, C-runtime-free compiler** with proper modularity.
