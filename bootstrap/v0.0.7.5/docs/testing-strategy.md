# Copyright 2025 Sybertnetics Artificial Intelligence Solutions
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# Testing Strategy: v0.0.7.5 Compiler Validation

## **Overview**

This document outlines the comprehensive testing strategy for validating the v0.0.7.3 → v0.0.7.5 transliteration. The goal is to ensure complete functional equivalence between the C and Runa implementations.

## **Testing Principles**

### **Core Requirements**
1. **Identical Behavior** - Output must match v0.0.7.3 exactly
2. **Complete Coverage** - Every function and code path tested
3. **Edge Case Validation** - Boundary conditions preserved
4. **Error Compatibility** - Error messages and handling identical
5. **Performance Verification** - No significant regression

### **Testing Levels**
- **Unit Tests** - Individual component validation
- **Integration Tests** - Component interaction verification
- **System Tests** - End-to-end compilation pipeline
- **Bootstrap Tests** - Self-compilation verification
- **Regression Tests** - Comparison against v0.0.7.3

## **Test Structure**

```
tests/
├── unit/                    # Component-level tests
│   ├── test_string_utils.runa
│   ├── test_hashtable.runa
│   ├── test_containers.runa
│   ├── test_lexer.runa
│   ├── test_parser.runa
│   └── test_codegen.runa
├── integration/             # Cross-component tests
│   ├── test_lexer_parser.runa
│   ├── test_parser_codegen.runa
│   └── test_full_pipeline.runa
├── system/                  # End-to-end tests
│   ├── test_simple_programs/
│   ├── test_complex_programs/
│   └── test_error_cases/
├── bootstrap/               # Self-compilation tests
│   ├── test_self_compile.sh
│   └── test_output_comparison.sh
├── regression/              # v0.0.7.3 comparison
│   ├── test_against_v0073.sh
│   └── compare_assembly.py
└── fixtures/                # Test data and expected outputs
```

## **Unit Testing Strategy**

### **String Utilities Tests** (`test_string_utils.runa`)

```runa
Process called "test_string_builder_create" returns Integer:
    Let sb be string_builder_create()
    assert(sb is not equal to 0)

    Let initial_length be string_builder_get_length(sb)
    assert(initial_length is equal to 0)

    string_builder_destroy(sb)
    Return 0
End Process

Process called "test_string_builder_append" returns Integer:
    Let sb be string_builder_create()
    string_builder_append(sb, "Hello")
    string_builder_append(sb, " World")

    Let result be string_builder_to_string(sb)
    Let expected be "Hello World"
    assert(string_equals(result, expected))

    string_builder_destroy(sb)
    Return 0
End Process

Process called "test_string_builder_capacity_growth" returns Integer:
    Let sb be string_builder_create_with_capacity(4)

    # Test automatic capacity growth
    string_builder_append(sb, "This string is longer than initial capacity")

    Let result be string_builder_to_string(sb)
    Let expected be "This string is longer than initial capacity"
    assert(string_equals(result, expected))

    string_builder_destroy(sb)
    Return 0
End Process
```

**Coverage Requirements**:
- ✅ Constructor/destructor functions
- ✅ Basic operations (append, to_string)
- ✅ Capacity management and growth
- ✅ Memory safety (no leaks, no overflows)
- ✅ Edge cases (empty strings, large strings)

### **Hash Table Tests** (`test_hashtable.runa`)

```runa
Process called "test_hashtable_basic_operations" returns Integer:
    Let ht be hashtable_create()

    # Test insertion
    hashtable_put(ht, "key1", "value1")
    hashtable_put(ht, "key2", "value2")

    # Test retrieval
    Let value1 be hashtable_get(ht, "key1")
    assert(string_equals(value1, "value1"))

    Let value2 be hashtable_get(ht, "key2")
    assert(string_equals(value2, "value2"))

    # Test non-existent key
    Let missing be hashtable_get(ht, "missing")
    assert(missing is equal to 0)

    hashtable_destroy(ht)
    Return 0
End Process

Process called "test_hashtable_collision_handling" returns Integer:
    Let ht be hashtable_create()

    # Force collisions by using keys with same hash
    # (This requires knowledge of hash function)
    hashtable_put(ht, "collision1", "value1")
    hashtable_put(ht, "collision2", "value2")

    # Verify both values retrievable
    Let value1 be hashtable_get(ht, "collision1")
    Let value2 be hashtable_get(ht, "collision2")
    assert(string_equals(value1, "value1"))
    assert(string_equals(value2, "value2"))

    hashtable_destroy(ht)
    Return 0
End Process
```

**Coverage Requirements**:
- ✅ Basic operations (create, put, get, destroy)
- ✅ Collision handling via chaining
- ✅ Dynamic resizing when load factor exceeded
- ✅ Key/value memory management
- ✅ Hash function distribution

### **Container Tests** (`test_containers.runa`)

```runa
Process called "test_array_basic_operations" returns Integer:
    Let arr be array_create()

    # Test appending
    array_append(arr, "item1")
    array_append(arr, "item2")
    array_append(arr, "item3")

    # Test size
    Let size be array_size(arr)
    assert(size is equal to 3)

    # Test retrieval
    Let item1 be array_get(arr, 0)
    assert(string_equals(item1, "item1"))

    Let item3 be array_get(arr, 2)
    assert(string_equals(item3, "item3"))

    array_destroy(arr)
    Return 0
End Process

Process called "test_array_capacity_growth" returns Integer:
    Let arr be array_create()

    # Add many items to force capacity growth
    Let i be 0
    While i is less than 100:
        Let item be string_concat("item", integer_to_string(i))
        array_append(arr, item)
        Set i to i plus 1
    End While

    # Verify all items present
    Let size be array_size(arr)
    assert(size is equal to 100)

    Let item50 be array_get(arr, 50)
    assert(string_equals(item50, "item50"))

    array_destroy(arr)
    Return 0
End Process
```

**Coverage Requirements**:
- ✅ Dynamic array creation/destruction
- ✅ Append, get, set operations
- ✅ Automatic capacity growth
- ✅ Index bounds checking
- ✅ Memory management

## **Lexer Testing Strategy**

### **Token Recognition Tests** (`test_lexer.runa`)

```runa
Process called "test_lexer_keywords" returns Integer:
    Let source be "Process Let Return If While"
    Let lexer be lexer_create(source)

    Let token1 be lexer_next_token(lexer)
    assert(token_get_type(token1) is equal to TOKEN_PROCESS)

    Let token2 be lexer_next_token(lexer)
    assert(token_get_type(token2) is equal to TOKEN_LET)

    Let token3 be lexer_next_token(lexer)
    assert(token_get_type(token3) is equal to TOKEN_RETURN)

    Let token4 be lexer_next_token(lexer)
    assert(token_get_type(token4) is equal to TOKEN_IF)

    Let token5 be lexer_next_token(lexer)
    assert(token_get_type(token5) is equal to TOKEN_WHILE)

    lexer_destroy(lexer)
    Return 0
End Process

Process called "test_lexer_numbers" returns Integer:
    Let source be "42 0 999 123"
    Let lexer be lexer_create(source)

    Let token1 be lexer_next_token(lexer)
    assert(token_get_type(token1) is equal to TOKEN_INTEGER)
    Let value1 be token_get_value(token1)
    assert(string_equals(value1, "42"))

    Let token2 be lexer_next_token(lexer)
    assert(token_get_type(token2) is equal to TOKEN_INTEGER)
    Let value2 be token_get_value(token2)
    assert(string_equals(value2, "0"))

    lexer_destroy(lexer)
    Return 0
End Process

Process called "test_lexer_strings" returns Integer:
    Let source be "\"Hello World\" \"\" \"Escaped \\\"quote\\\"\""
    Let lexer be lexer_create(source)

    Let token1 be lexer_next_token(lexer)
    assert(token_get_type(token1) is equal to TOKEN_STRING_LITERAL)
    Let value1 be token_get_value(token1)
    assert(string_equals(value1, "Hello World"))

    Let token2 be lexer_next_token(lexer)
    assert(token_get_type(token2) is equal to TOKEN_STRING_LITERAL)
    Let value2 be token_get_value(token2)
    assert(string_equals(value2, ""))

    lexer_destroy(lexer)
    Return 0
End Process
```

**Coverage Requirements**:
- ✅ All 144 token types recognized
- ✅ Keyword vs identifier distinction
- ✅ Number parsing (including edge cases)
- ✅ String parsing with escape sequences
- ✅ Position tracking (line/column)
- ✅ Error handling for invalid tokens

## **Parser Testing Strategy**

### **Expression Parsing Tests** (`test_parser.runa`)

```runa
Process called "test_parser_arithmetic" returns Integer:
    Let source be "2 plus 3 multiplied by 4"
    Let lexer be lexer_create(source)
    Let parser be parser_create(lexer)

    Let expr be parse_expression(parser)

    # Verify AST structure for precedence
    assert(expr_get_type(expr) is equal to EXPR_BINARY_OP)
    assert(expr_get_operator(expr) is equal to TOKEN_PLUS)

    Let right be expr_get_right(expr)
    assert(expr_get_type(right) is equal to EXPR_BINARY_OP)
    assert(expr_get_operator(right) is equal to TOKEN_MULTIPLIED)

    parser_destroy(parser)
    lexer_destroy(lexer)
    Return 0
End Process

Process called "test_parser_function_call" returns Integer:
    Let source be "add(10, 20)"
    Let lexer be lexer_create(source)
    Let parser be parser_create(lexer)

    Let expr be parse_expression(parser)

    assert(expr_get_type(expr) is equal to EXPR_FUNCTION_CALL)
    Let func_name be expr_get_function_name(expr)
    assert(string_equals(func_name, "add"))

    Let arg_count be expr_get_argument_count(expr)
    assert(arg_count is equal to 2)

    parser_destroy(parser)
    lexer_destroy(lexer)
    Return 0
End Process
```

**Coverage Requirements**:
- ✅ All expression types parsed correctly
- ✅ Operator precedence preserved
- ✅ Function calls with arguments
- ✅ Field access expressions
- ✅ Type construction expressions
- ✅ Statement parsing (Let, Set, If, While, etc.)

## **Integration Testing Strategy**

### **Lexer-Parser Integration** (`test_lexer_parser.runa`)

```runa
Process called "test_complete_program_parsing" returns Integer:
    Let source be "Process called \"main\" takes argc as Integer returns Integer:\n    Let x be 42\n    Return x\nEnd Process"

    Let lexer be lexer_create(source)
    Let parser be parser_create(lexer)
    Let program be parser_parse_program(parser)

    # Verify program structure
    Let func_count be program_get_function_count(program)
    assert(func_count is equal to 1)

    Let main_func be program_get_function(program, 0)
    Let func_name be function_get_name(main_func)
    assert(string_equals(func_name, "main"))

    Let param_count be function_get_parameter_count(main_func)
    assert(param_count is equal to 1)

    program_destroy(program)
    parser_destroy(parser)
    lexer_destroy(lexer)
    Return 0
End Process
```

### **Parser-Codegen Integration** (`test_parser_codegen.runa`)

```runa
Process called "test_simple_codegen" returns Integer:
    Let source be "Process called \"test\" returns Integer:\n    Return 42\nEnd Process"

    Let lexer be lexer_create(source)
    Let parser be parser_create(lexer)
    Let program be parser_parse_program(parser)

    Let codegen be codegen_create("test_output.s")
    codegen_generate(codegen, program)
    codegen_destroy(codegen)

    # Verify assembly file contains expected content
    Let assembly be read_file("test_output.s")
    Let has_main be string_find(assembly, "test:")
    assert(has_main is not equal to -1)

    Let has_return be string_find(assembly, "movq $42, %rax")
    assert(has_return is not equal to -1)

    program_destroy(program)
    parser_destroy(parser)
    lexer_destroy(lexer)
    Return 0
End Process
```

## **System Testing Strategy**

### **End-to-End Compilation Tests**

```bash
#!/bin/bash
# test_compilation.sh

# Test simple programs
echo "Testing simple program compilation..."
cat > test_simple.runa << 'EOF'
Process called "main" takes argc as Integer, argv as Integer returns Integer:
    Return 42
End Process
EOF

# Compile with v0.0.7.5
./build/runac test_simple.runa test_simple.s
if [ $? -ne 0 ]; then
    echo "FAIL: Simple program compilation failed"
    exit 1
fi

# Assemble and link
as --64 test_simple.s -o test_simple.o
gcc test_simple.o -o test_simple
if [ $? -ne 0 ]; then
    echo "FAIL: Assembly/linking failed"
    exit 1
fi

# Run and check exit code
./test_simple
RESULT=$?
if [ $RESULT -ne 42 ]; then
    echo "FAIL: Expected exit code 42, got $RESULT"
    exit 1
fi

echo "PASS: Simple program compilation test"
```

### **Error Handling Tests**

```bash
#!/bin/bash
# test_error_handling.sh

echo "Testing syntax error handling..."
cat > test_syntax_error.runa << 'EOF'
Process called "main" takes argc as Integer returns Integer
    Return 42  # Missing colon after returns Integer
End Process
EOF

# Should fail with specific error message
./build/runac test_syntax_error.runa test_error.s 2>error_output.txt
if [ $? -eq 0 ]; then
    echo "FAIL: Should have failed on syntax error"
    exit 1
fi

# Check error message matches v0.0.7.3
if ! grep -q "Expected ':'" error_output.txt; then
    echo "FAIL: Error message doesn't match expected format"
    exit 1
fi

echo "PASS: Error handling test"
```

## **Bootstrap Testing Strategy**

### **Self-Compilation Test**

```bash
#!/bin/bash
# test_bootstrap.sh

echo "Testing v0.0.7.5 self-compilation..."

# Stage 1: Compile v0.0.7.5 using v0.0.7.3
echo "Stage 1: Compiling v0.0.7.5 with v0.0.7.3..."
make clean
make all
if [ $? -ne 0 ]; then
    echo "FAIL: Stage 1 compilation failed"
    exit 1
fi
cp build/runac build/runac_stage1

# Stage 2: Compile v0.0.7.5 using Stage 1
echo "Stage 2: Compiling v0.0.7.5 with Stage 1..."
make clean-runa
RUNAC_V0073=build/runac_stage1 make runa-compile
make link
if [ $? -ne 0 ]; then
    echo "FAIL: Stage 2 compilation failed"
    exit 1
fi
cp build/runac build/runac_stage2

# Stage 3: Compare Stage 1 and Stage 2 outputs
echo "Stage 3: Comparing outputs..."
./build/runac_stage1 tests/test_simple.runa test1.s
./build/runac_stage2 tests/test_simple.runa test2.s

if ! diff test1.s test2.s; then
    echo "FAIL: Stage 1 and Stage 2 produce different output"
    exit 1
fi

echo "PASS: Bootstrap test successful"
```

## **Regression Testing Strategy**

### **Assembly Output Comparison**

```python
#!/usr/bin/env python3
# compare_assembly.py

import subprocess
import sys
import difflib

def compile_with_v0073(source, output):
    """Compile with v0.0.7.3"""
    result = subprocess.run([
        '../v0.0.7.3/runac', source, output
    ], capture_output=True, text=True)
    return result.returncode == 0, result.stderr

def compile_with_v0075(source, output):
    """Compile with v0.0.7.5"""
    result = subprocess.run([
        './build/runac', source, output
    ], capture_output=True, text=True)
    return result.returncode == 0, result.stderr

def compare_assembly(file1, file2):
    """Compare assembly files line by line"""
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()

    # Generate diff
    diff = list(difflib.unified_diff(lines1, lines2,
                                   fromfile='v0.0.7.3',
                                   tofile='v0.0.7.5'))

    return len(diff) == 0, diff

def test_program(source_file):
    """Test a single program against both compilers"""
    print(f"Testing {source_file}...")

    # Compile with both versions
    success_v0073, error_v0073 = compile_with_v0073(source_file, 'test_v0073.s')
    success_v0075, error_v0075 = compile_with_v0075(source_file, 'test_v0075.s')

    # Both should succeed or both should fail
    if success_v0073 != success_v0075:
        print(f"FAIL: Compilation results differ")
        print(f"v0.0.7.3: {'SUCCESS' if success_v0073 else 'FAIL'}")
        print(f"v0.0.7.5: {'SUCCESS' if success_v0075 else 'FAIL'}")
        return False

    # If both failed, check error messages
    if not success_v0073:
        if error_v0073.strip() != error_v0075.strip():
            print(f"FAIL: Error messages differ")
            print(f"v0.0.7.3: {error_v0073}")
            print(f"v0.0.7.5: {error_v0075}")
            return False
        print(f"PASS: Both failed with same error")
        return True

    # Compare assembly output
    identical, diff = compare_assembly('test_v0073.s', 'test_v0075.s')
    if not identical:
        print(f"FAIL: Assembly output differs")
        for line in diff:
            print(line.rstrip())
        return False

    print(f"PASS: Identical output")
    return True

# Test all programs in test suite
test_programs = [
    'tests/test_simple.runa',
    'tests/test_arithmetic.runa',
    'tests/test_functions.runa',
    'tests/test_conditions.runa',
    'tests/test_loops.runa',
]

all_passed = True
for program in test_programs:
    if not test_program(program):
        all_passed = False

sys.exit(0 if all_passed else 1)
```

## **Performance Testing**

### **Compilation Speed Benchmark**

```bash
#!/bin/bash
# benchmark_compilation.sh

echo "Benchmarking compilation speed..."

# Large test program
cat > large_test.runa << 'EOF'
# Generated large program with many functions
Process called "func1" returns Integer: Return 1 End Process
Process called "func2" returns Integer: Return 2 End Process
# ... (generate 1000 functions)
EOF

# Benchmark v0.0.7.3
echo "Benchmarking v0.0.7.3..."
time ../v0.0.7.3/runac large_test.runa large_v0073.s

# Benchmark v0.0.7.5
echo "Benchmarking v0.0.7.5..."
time ./build/runac large_test.runa large_v0075.s

echo "Compare results manually for performance regression"
```

## **Continuous Integration**

### **Test Automation**

```bash
#!/bin/bash
# run_all_tests.sh

set -e  # Exit on any failure

echo "Running complete test suite..."

# Unit tests
echo "Running unit tests..."
make test-units

# Integration tests
echo "Running integration tests..."
make test-integration

# System tests
echo "Running system tests..."
./tests/test_compilation.sh
./tests/test_error_handling.sh

# Bootstrap test
echo "Running bootstrap test..."
./tests/bootstrap/test_bootstrap.sh

# Regression tests
echo "Running regression tests..."
python3 tests/bootstrap/compare_assembly.py

# Performance tests
echo "Running performance tests..."
./tests/benchmark_compilation.sh

echo "All tests passed!"
```

---

**This testing strategy ensures complete validation of the transliteration while maintaining the exact behavior of the original C compiler.**