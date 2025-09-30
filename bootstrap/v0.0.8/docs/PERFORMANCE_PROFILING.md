# Performance Profiling Guide for v0.0.8

## Problem Statement

v0.0.7.5 exhibits O(n²) compilation time for large files:
- parser.runa (1200 LOC) fails to compile in 10 seconds
- codegen.runa (2600 LOC) fails to compile in 10 seconds
- Small files compile quickly (main.runa: 45ms)

This suggests algorithmic complexity issues, not constant-factor slowness.

## Profiling Strategy

### Step 1: Instrumentation

Add timing measurements to suspected hot functions:

```runa
# At module level
Let global_timer_start be 0
Let global_timer_calls be 0

# At function entry
Process called "suspected_slow_function":
    Let global_timer_calls be global_timer_calls plus 1
    # ... function body ...
```

Then measure:
```bash
time ./build/runac src/parser.runa /tmp/test.s
```

Compare call counts for small vs large files to detect exponential growth.

### Step 2: Likely Suspects

Based on v0.0.7.5 architecture, these are prime candidates:

#### Suspect 1: Variable Lookup (parser.runa)

**Location:** parser_parse_expression, parser_parse_primary

**Current implementation (suspected):**
```runa
Process called "parser_find_variable":
    Let i be 0
    While i is less than variable_count:
        # Linear search through all variables
        Let var be variables[i]
        If name matches var_name:
            Return var
        Let i be i plus 1
    Return 0
```

**Complexity:** O(n) per lookup, called O(n) times = O(n²)

**Fix:** Use hashtable for O(1) lookup

#### Suspect 2: Statement Iteration (codegen.runa)

**Location:** codegen_generate_function, codegen_generate_statement

**Current implementation (suspected):**
```runa
Process called "codegen_generate_function":
    For each function in program:  # O(n)
        For each statement in function:  # O(m)
            For each nested statement:  # O(k)
                codegen_generate_statement()  # May have internal loops
```

**Complexity:** O(n * m * k) worst case

**Fix:** Flatten statement processing with explicit stack

#### Suspect 3: String Operations (both modules)

**Location:** emit_line, codegen_generate_*

**Current implementation (suspected):**
```runa
Process called "build_assembly_line":
    Let result be ""
    Let result be string_concat(result, "movq ")
    Let result be string_concat(result, register)
    Let result be string_concat(result, ", ")
    Let result be string_concat(result, operand)
    # Each concat allocates new string = O(n²)
```

**Complexity:** O(n²) for n concatenations

**Fix:** String buffer with pre-allocation

#### Suspect 4: Type Calculations (codegen.runa)

**Location:** codegen_calculate_type_size

**Current implementation (suspected):**
```runa
Process called "codegen_calculate_type_size":
    # Called repeatedly for same types
    # No caching = redundant work
    Search through all types linearly
    Calculate size each time
```

**Complexity:** O(t) per call, called O(n) times = O(n*t)

**Fix:** Cache type sizes in hashtable

### Step 3: Verification

After identifying suspects, verify with:

**Method 1: Differential timing**
```bash
# Small file (fast)
time ./build/runac tests/unit/test_minimal.runa /tmp/test1.s

# Medium file (slower)
time ./build/runac src/lexer.runa /tmp/test2.s

# Large file (very slow)
time ./build/runac src/parser.runa /tmp/test3.s
```

If time grows quadratically with LOC, hypothesis confirmed.

**Method 2: Call counting**
Add counters to suspected functions and compare:

| Function | Calls (100 LOC) | Calls (1000 LOC) | Growth |
|----------|-----------------|------------------|---------|
| lookup_variable | 100 | 10,000 | O(n²) |
| generate_statement | 100 | 1,000 | O(n) |

## Optimization Techniques

### Technique 1: Hashtable-Based Symbol Tables

**Before:**
```runa
# Linear array of variables
Let variables be allocate(max_variables multiplied by 32)
Let variable_count be 0

Process called "add_variable":
    # Store at end of array
    Let offset be variable_count multiplied by 32
    memory_set_pointer(variables plus offset, name)
    Let variable_count be variable_count plus 1

Process called "find_variable":
    Let i be 0
    While i is less than variable_count:  # O(n)
        Let offset be i multiplied by 32
        Let var_name be memory_get_pointer(variables plus offset, 0)
        If string_equals(var_name, name):
            Return variables plus offset
        Let i be i plus 1
    Return 0
```

**After:**
```runa
# Hashtable-based symbol table
Let symbol_table be hashtable_create(64)

Process called "add_variable":
    # O(1) insertion
    hashtable_set(symbol_table, name, variable_pointer)

Process called "find_variable":
    # O(1) lookup
    Return hashtable_get(symbol_table, name)
```

**Improvement:** O(n²) → O(n)

### Technique 2: Statement Stack Instead of Recursion

**Before:**
```runa
Process called "process_statements":
    Let i be 0
    While i is less than statement_count:
        Let stmt be statements[i]
        Let stmt_type be memory_get_int32(stmt, 0)

        If stmt_type is equal to STMT_IF:
            # Recursively process body statements
            Let body_count be memory_get_int32(stmt, 16)
            Let body be memory_get_pointer(stmt, 24)
            process_statements(body, body_count)  # Recursive

            Let else_count be memory_get_int32(stmt, 32)
            Let else_body be memory_get_pointer(stmt, 40)
            process_statements(else_body, else_count)  # Recursive

        Let i be i plus 1
```

**After:**
```runa
Process called "process_statements_iterative":
    Let stack be allocate_stack(1000)
    push_statements(stack, statements, statement_count)

    While stack_not_empty(stack):
        Let stmt be stack_pop(stack)
        Let stmt_type be memory_get_int32(stmt, 0)

        If stmt_type is equal to STMT_IF:
            Let else_body be memory_get_pointer(stmt, 40)
            Let else_count be memory_get_int32(stmt, 32)
            push_statements(stack, else_body, else_count)

            Let body be memory_get_pointer(stmt, 24)
            Let body_count be memory_get_int32(stmt, 16)
            push_statements(stack, body, body_count)
```

**Improvement:** Better cache locality, no recursion overhead

### Technique 3: String Buffer

**Before:**
```runa
Process called "emit_instruction":
    Let result be "    "
    Let result be string_concat(result, opcode)
    Let result be string_concat(result, " ")
    Let result be string_concat(result, operand1)
    Let result be string_concat(result, ", ")
    Let result be string_concat(result, operand2)
    file_write_fd(output, result, 0)
    # 6 allocations per instruction
```

**After:**
```runa
# Write directly to file, no intermediate string
Process called "emit_instruction":
    file_write_fd(output, "    ", 0)
    file_write_fd(output, opcode, 0)
    file_write_fd(output, " ", 0)
    file_write_fd(output, operand1, 0)
    file_write_fd(output, ", ", 0)
    file_write_fd(output, operand2, 0)
    # 6 writes, no allocations
```

**Improvement:** O(n²) → O(n), no memory allocation

### Technique 4: Type Size Cache

**Before:**
```runa
Process called "codegen_calculate_type_size":
    # Called repeatedly for "Integer", "String", etc.
    If type_name is equal to "Integer":
        Return 8
    If type_name is equal to "String":
        Return 8
    # ... search all custom types linearly
```

**After:**
```runa
# At codegen initialization
Let type_size_cache be hashtable_create(64)
hashtable_set(type_size_cache, "Integer", 8)
hashtable_set(type_size_cache, "String", 8)

Process called "codegen_calculate_type_size":
    Let cached be hashtable_get(type_size_cache, type_name)
    If cached is not equal to 0:
        Return cached
    # Calculate and cache custom types
    Let size be calculate_custom_type_size(type_name)
    hashtable_set(type_size_cache, type_name, size)
    Return size
```

**Improvement:** Amortized O(1) instead of O(t)

## Measurement and Validation

### Before Optimization

Record baseline measurements:
```bash
# Create baseline file
echo "=== v0.0.7.5 Baseline ===" > performance_log.txt
echo "Date: $(date)" >> performance_log.txt

# Small file
(time ./build/runac tests/unit/test_minimal.runa /tmp/test1.s) 2>> performance_log.txt

# Medium file
(time ./build/runac src/lexer.runa /tmp/test2.s) 2>> performance_log.txt

# Large file (may timeout)
timeout 60s time ./build/runac src/parser.runa /tmp/test3.s 2>> performance_log.txt || echo "TIMEOUT" >> performance_log.txt
```

### After Each Optimization

Re-run measurements and compare:
```bash
echo "=== After Optimization X ===" >> performance_log.txt
# ... repeat tests ...
```

### Success Criteria

Target improvements:
- parser.runa: >10s → <5s (>50% improvement)
- codegen.runa: >10s → <5s (>50% improvement)
- lexer.runa: 1.17s → <1s (>15% improvement)
- Full self-compile: unmeasurable → <10s

## Tools

### Valgrind Profiling

```bash
valgrind --tool=callgrind --callgrind-out-file=callgrind.out ./build/runac src/parser.runa /tmp/test.s
callgrind_annotate callgrind.out
```

Look for:
- Functions with high "Ir" (instruction reads) = CPU-bound
- Functions called many times = potential O(n²)

### Manual Instrumentation

Add to suspected functions:
```runa
# At start of function
Let function_call_count be function_call_count plus 1

# Periodically print
If function_call_count modulo by 1000 is equal to 0:
    print_string("Function called ")
    print_integer(function_call_count)
    print_string(" times")
```

If call count grows quadratically with input size, found the culprit.

## Expected Results

After all optimizations:

| File | LOC | v0.0.7.5 | v0.0.8 Target | Speedup |
|------|-----|----------|---------------|---------|
| test_minimal.runa | 5 | 45ms | 40ms | 1.1x |
| test_let.runa | 10 | 50ms | 45ms | 1.1x |
| lexer.runa | 800 | 1.17s | 800ms | 1.5x |
| parser.runa | 1200 | >10s | 4s | >2.5x |
| codegen.runa | 2600 | >10s | 8s | >1.25x |
| **Full self-compile** | **~5000** | **>60s** | **<10s** | **>6x** |

## Next Steps

1. Copy v0.0.7.5 to v0.0.8
2. Add instrumentation to parser.runa
3. Identify top 3 hotspots
4. Apply targeted optimizations
5. Validate with bootstrap test
6. Move to next hotspot

Iterate until all targets met.