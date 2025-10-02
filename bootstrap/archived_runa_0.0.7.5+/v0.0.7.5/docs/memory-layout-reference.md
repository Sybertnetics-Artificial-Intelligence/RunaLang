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
# Memory Layout Reference for v0.0.7.5 Transliteration

This document defines the correct memory layout and access patterns for all data structures in the v0.0.7.5 Runa bootstrap compiler, based on the C implementations in v0.0.7.3.

## Critical Issue

The v0.0.7.5 transliteration systematically uses `memory_set_integer` and `memory_get_integer` for ALL fields, when pointer fields must use `memory_set_pointer` and `memory_get_pointer`. This document provides the correct mappings.

## Memory Access Rules

- **Pointer fields**: Use `memory_set_pointer` and `memory_get_pointer`
- **Integer fields**: Use `memory_set_integer` and `memory_get_integer`
- **Enum fields**: Use `memory_set_integer` and `memory_get_integer` (enums are integers in C)
- **Character fields**: Use `memory_set_integer` and `memory_get_integer` (chars are small integers)

## Core Data Structures

### Token Structure
```c
typedef struct {
    TokenType type;    // enum (int) - 4 bytes at offset 0
    char *value;       // pointer - 8 bytes at offset 8
    int line;          // int - 4 bytes at offset 16
    int column;        // int - 4 bytes at offset 20
} Token;               // Total size: 24 bytes (with padding)
```

**Runa Memory Access:**
- `type`: `memory_set_integer(token, 0, type)` / `memory_get_integer(token, 0)`
- `value`: `memory_set_pointer(token, 8, value)` / `memory_get_pointer(token, 8)`
- `line`: `memory_set_integer(token, 16, line)` / `memory_get_integer(token, 16)`
- `column`: `memory_set_integer(token, 20, column)` / `memory_get_integer(token, 20)`

### Lexer Structure
```c
typedef struct {
    char *source;      // pointer - 8 bytes at offset 0
    int position;      // int - 4 bytes at offset 8
    int line;          // int - 4 bytes at offset 12
    int column;        // int - 4 bytes at offset 16
    char current_char; // char - 1 byte at offset 20 (padded to 8 bytes)
} Lexer;               // Total size: 24 bytes
```

**Runa Memory Access:**
- `source`: `memory_set_pointer(lexer, 0, source)` / `memory_get_pointer(lexer, 0)`
- `position`: `memory_set_integer(lexer, 8, position)` / `memory_get_integer(lexer, 8)`
- `line`: `memory_set_integer(lexer, 12, line)` / `memory_get_integer(lexer, 12)`
- `column`: `memory_set_integer(lexer, 16, column)` / `memory_get_integer(lexer, 16)`
- `current_char`: `memory_set_integer(lexer, 20, current_char)` / `memory_get_integer(lexer, 20)`

**Note**: Current v0.0.7.5 uses wrong offsets - should be 12, 16, 20, not 16, 24, 32.

### Parser Structure
```c
typedef struct {
    Lexer *lexer;           // pointer - 8 bytes at offset 0
    Token *current_token;   // pointer - 8 bytes at offset 8
    Program *current_program; // pointer - 8 bytes at offset 16
} Parser;                   // Total size: 24 bytes
```

**Runa Memory Access:**
- `lexer`: `memory_set_pointer(parser, 0, lexer)` / `memory_get_pointer(parser, 0)`
- `current_token`: `memory_set_pointer(parser, 8, token)` / `memory_get_pointer(parser, 8)`
- `current_program`: `memory_set_pointer(parser, 16, program)` / `memory_get_pointer(parser, 16)`

### Expression Structure
```c
typedef struct Expression {
    ExpressionType type;    // enum (int) - 4 bytes at offset 0 (padded to 8)
    union {                 // Union starts at offset 8
        int integer_value;                    // int at offset 8
        char *variable_name;                  // pointer at offset 8
        char *string_literal;                 // pointer at offset 8
        char *type_name;                      // pointer at offset 8
        struct {
            struct Expression *left;          // pointer at offset 8
            struct Expression *right;         // pointer at offset 16
            TokenType operator;               // int at offset 24
        } binary_op;
        struct {
            struct Expression *object;        // pointer at offset 8
            char *field_name;                 // pointer at offset 16
        } field_access;
        struct {
            char *function_name;              // pointer at offset 8
            struct Expression **arguments;    // pointer at offset 16
            int argument_count;               // int at offset 24
        } function_call;
        struct {
            struct Expression *array;         // pointer at offset 8
            struct Expression *index;         // pointer at offset 16
        } array_index;
        // Other union members...
    } data;
} Expression;               // Total size: 32 bytes
```

**Runa Memory Access:**
- `type`: `memory_set_integer(expr, 0, type)` / `memory_get_integer(expr, 0)`
- **For binary_op:**
  - `left`: `memory_set_pointer(expr, 8, left)` / `memory_get_pointer(expr, 8)`
  - `right`: `memory_set_pointer(expr, 16, right)` / `memory_get_pointer(expr, 16)`
  - `operator`: `memory_set_integer(expr, 24, operator)` / `memory_get_integer(expr, 24)`
- **For field_access:**
  - `object`: `memory_set_pointer(expr, 8, object)` / `memory_get_pointer(expr, 8)`
  - `field_name`: `memory_set_pointer(expr, 16, field_name)` / `memory_get_pointer(expr, 16)`
- **For function_call:**
  - `function_name`: `memory_set_pointer(expr, 8, function_name)` / `memory_get_pointer(expr, 8)`
  - `arguments`: `memory_set_pointer(expr, 16, arguments)` / `memory_get_pointer(expr, 16)`
  - `argument_count`: `memory_set_integer(expr, 24, count)` / `memory_get_integer(expr, 24)`
- **For array_index:**
  - `array`: `memory_set_pointer(expr, 8, array)` / `memory_get_pointer(expr, 8)`
  - `index`: `memory_set_pointer(expr, 16, index)` / `memory_get_pointer(expr, 16)`

### Statement Structure
```c
typedef struct Statement {
    StatementType type;     // enum (int) - 4 bytes at offset 0 (padded to 8)
    union {                 // Union starts at offset 8
        struct {
            char *variable_name;              // pointer at offset 8
            Expression *expression;           // pointer at offset 16
        } let_stmt;
        struct {
            Expression *target;               // pointer at offset 8
            Expression *expression;           // pointer at offset 16
        } set_stmt;
        struct {
            Expression *expression;           // pointer at offset 8
        } return_stmt;
        struct {
            Expression *condition;            // pointer at offset 8
            struct Statement **if_body;       // pointer at offset 16
            int if_body_count;                // int at offset 24
            struct Statement **else_body;     // pointer at offset 32
            int else_body_count;              // int at offset 40
        } if_stmt;
        struct {
            Expression *condition;            // pointer at offset 8
            struct Statement **body;          // pointer at offset 16
            int body_count;                   // int at offset 24
        } while_stmt;
        struct {
            Expression *expression;           // pointer at offset 8
        } print_stmt;
        struct {
            Expression *expression;           // pointer at offset 8
        } expr_stmt;
        // Other union members...
    } data;
} Statement;                // Total size: 48 bytes
```

**Runa Memory Access:**
- `type`: `memory_set_integer(stmt, 0, type)` / `memory_get_integer(stmt, 0)`
- **For let_stmt:**
  - `variable_name`: `memory_set_pointer(stmt, 8, name)` / `memory_get_pointer(stmt, 8)`
  - `expression`: `memory_set_pointer(stmt, 16, expr)` / `memory_get_pointer(stmt, 16)`
- **For set_stmt:**
  - `target`: `memory_set_pointer(stmt, 8, target)` / `memory_get_pointer(stmt, 8)`
  - `expression`: `memory_set_pointer(stmt, 16, expr)` / `memory_get_pointer(stmt, 16)`
- **For if_stmt:**
  - `condition`: `memory_set_pointer(stmt, 8, condition)` / `memory_get_pointer(stmt, 8)`
  - `if_body`: `memory_set_pointer(stmt, 16, if_body)` / `memory_get_pointer(stmt, 16)`
  - `if_body_count`: `memory_set_integer(stmt, 24, count)` / `memory_get_integer(stmt, 24)`
  - `else_body`: `memory_set_pointer(stmt, 32, else_body)` / `memory_get_pointer(stmt, 32)`
  - `else_body_count`: `memory_set_integer(stmt, 40, count)` / `memory_get_integer(stmt, 40)`

### Function Structure
```c
typedef struct {
    char *name;                // pointer - 8 bytes at offset 0
    Parameter *parameters;     // pointer - 8 bytes at offset 8
    int parameter_count;       // int - 4 bytes at offset 16 (padded to 8)
    char *return_type;         // pointer - 8 bytes at offset 24
    Statement **statements;    // pointer - 8 bytes at offset 32
    int statement_count;       // int - 4 bytes at offset 40 (padded to 8)
} Function;                    // Total size: 48 bytes
```

**Runa Memory Access:**
- `name`: `memory_set_pointer(func, 0, name)` / `memory_get_pointer(func, 0)`
- `parameters`: `memory_set_pointer(func, 8, parameters)` / `memory_get_pointer(func, 8)`
- `parameter_count`: `memory_set_integer(func, 16, count)` / `memory_get_integer(func, 16)`
- `return_type`: `memory_set_pointer(func, 24, return_type)` / `memory_get_pointer(func, 24)`
- `statements`: `memory_set_pointer(func, 32, statements)` / `memory_get_pointer(func, 32)`
- `statement_count`: `memory_set_integer(func, 40, count)` / `memory_get_integer(func, 40)`

### Program Structure
```c
typedef struct {
    Function **functions;      // pointer - 8 bytes at offset 0
    int function_count;        // int - 4 bytes at offset 8
    int function_capacity;     // int - 4 bytes at offset 12
    TypeDefinition **types;    // pointer - 8 bytes at offset 16
    int type_count;            // int - 4 bytes at offset 24
    int type_capacity;         // int - 4 bytes at offset 28
    Import **imports;          // pointer - 8 bytes at offset 32
    int import_count;          // int - 4 bytes at offset 40
    int import_capacity;       // int - 4 bytes at offset 44
    GlobalVariable **globals;  // pointer - 8 bytes at offset 48
    int global_count;          // int - 4 bytes at offset 56
    int global_capacity;       // int - 4 bytes at offset 60
} Program;                     // Total size: 64 bytes
```

**Runa Memory Access:**
- `functions`: `memory_set_pointer(program, 0, functions)` / `memory_get_pointer(program, 0)`
- `function_count`: `memory_set_integer(program, 8, count)` / `memory_get_integer(program, 8)`
- `function_capacity`: `memory_set_integer(program, 12, capacity)` / `memory_get_integer(program, 12)`
- `types`: `memory_set_pointer(program, 16, types)` / `memory_get_pointer(program, 16)`
- `type_count`: `memory_set_integer(program, 24, count)` / `memory_get_integer(program, 24)`
- `type_capacity`: `memory_set_integer(program, 28, capacity)` / `memory_get_integer(program, 28)`
- `imports`: `memory_set_pointer(program, 32, imports)` / `memory_get_pointer(program, 32)`
- `import_count`: `memory_set_integer(program, 40, count)` / `memory_get_integer(program, 40)`
- `import_capacity`: `memory_set_integer(program, 44, capacity)` / `memory_get_integer(program, 44)`
- `globals`: `memory_set_pointer(program, 48, globals)` / `memory_get_pointer(program, 48)`
- `global_count`: `memory_set_integer(program, 56, count)` / `memory_get_integer(program, 56)`
- `global_capacity`: `memory_set_integer(program, 60, capacity)` / `memory_get_integer(program, 60)`

## String Utils Structures

### StringBuilder Structure
```c
typedef struct StringBuilder {
    char* buffer;       // pointer - 8 bytes at offset 0
    size_t capacity;    // int - 8 bytes at offset 8
    size_t length;      // int - 8 bytes at offset 16
} StringBuilder;        // Total size: 24 bytes
```

**Runa Memory Access:**
- `buffer`: `memory_set_pointer(sb, 0, buffer)` / `memory_get_pointer(sb, 0)`
- `capacity`: `memory_set_integer(sb, 8, capacity)` / `memory_get_integer(sb, 8)`
- `length`: `memory_set_integer(sb, 16, length)` / `memory_get_integer(sb, 16)`

### StringTokenizer Structure
```c
typedef struct StringTokenizer {
    char* string;           // pointer - 8 bytes at offset 0
    char* current;          // pointer - 8 bytes at offset 8
    const char* delimiters; // pointer - 8 bytes at offset 16
    bool own_string;        // int (bool) - 4 bytes at offset 24 (padded to 8)
} StringTokenizer;          // Total size: 32 bytes
```

**Runa Memory Access:**
- `string`: `memory_set_pointer(tokenizer, 0, string)` / `memory_get_pointer(tokenizer, 0)`
- `current`: `memory_set_pointer(tokenizer, 8, current)` / `memory_get_pointer(tokenizer, 8)`
- `delimiters`: `memory_set_pointer(tokenizer, 16, delimiters)` / `memory_get_pointer(tokenizer, 16)`
- `own_string`: `memory_set_integer(tokenizer, 24, own_string)` / `memory_get_integer(tokenizer, 24)`

### StringArray Structure
```c
typedef struct StringArray {
    char** strings;     // pointer - 8 bytes at offset 0
    size_t count;       // int - 8 bytes at offset 8
    size_t capacity;    // int - 8 bytes at offset 16
} StringArray;          // Total size: 24 bytes
```

**Runa Memory Access:**
- `strings`: `memory_set_pointer(arr, 0, strings)` / `memory_get_pointer(arr, 0)`
- `count`: `memory_set_integer(arr, 8, count)` / `memory_get_integer(arr, 8)`
- `capacity`: `memory_set_integer(arr, 16, capacity)` / `memory_get_integer(arr, 16)`

## Container Structures

### Vector Structure
```c
typedef struct Vector {
    void** items;           // pointer - 8 bytes at offset 0
    size_t capacity;        // int - 8 bytes at offset 8
    size_t size;           // int - 8 bytes at offset 16
    void (*free_item)(void*); // function pointer - 8 bytes at offset 24
} Vector;                   // Total size: 32 bytes
```

**Runa Memory Access:**
- `items`: `memory_set_pointer(vec, 0, items)` / `memory_get_pointer(vec, 0)`
- `capacity`: `memory_set_integer(vec, 8, capacity)` / `memory_get_integer(vec, 8)`
- `size`: `memory_set_integer(vec, 16, size)` / `memory_get_integer(vec, 16)`
- `free_item`: `memory_set_pointer(vec, 24, free_item)` / `memory_get_pointer(vec, 24)`

### LinkedList Structure
```c
typedef struct LinkedList {
    ListNode* head;         // pointer - 8 bytes at offset 0
    ListNode* tail;         // pointer - 8 bytes at offset 8
    size_t size;           // int - 8 bytes at offset 16
    void (*free_item)(void*); // function pointer - 8 bytes at offset 24
} LinkedList;               // Total size: 32 bytes
```

**Runa Memory Access:**
- `head`: `memory_set_pointer(list, 0, head)` / `memory_get_pointer(list, 0)`
- `tail`: `memory_set_pointer(list, 8, tail)` / `memory_get_pointer(list, 8)`
- `size`: `memory_set_integer(list, 16, size)` / `memory_get_integer(list, 16)`
- `free_item`: `memory_set_pointer(list, 24, free_item)` / `memory_get_pointer(list, 24)`

## HashTable Structures

### HashEntry Structure
```c
struct HashEntry {
    void* key;          // pointer - 8 bytes at offset 0
    void* value;        // pointer - 8 bytes at offset 8
    HashEntry* next;    // pointer - 8 bytes at offset 16
};                      // Total size: 24 bytes
```

**Runa Memory Access:**
- `key`: `memory_set_pointer(entry, 0, key)` / `memory_get_pointer(entry, 0)`
- `value`: `memory_set_pointer(entry, 8, value)` / `memory_get_pointer(entry, 8)`
- `next`: `memory_set_pointer(entry, 16, next)` / `memory_get_pointer(entry, 16)`

### HashTable Structure
```c
struct HashTable {
    HashEntry** buckets;       // pointer - 8 bytes at offset 0
    size_t bucket_count;        // int - 8 bytes at offset 8
    size_t entry_count;         // int - 8 bytes at offset 16
    HashFunction hash_func;     // function pointer - 8 bytes at offset 24
    CompareFunction compare_func; // function pointer - 8 bytes at offset 32
    FreeKeyFunction free_key;   // function pointer - 8 bytes at offset 40
    FreeValueFunction free_value; // function pointer - 8 bytes at offset 48
};                             // Total size: 56 bytes
```

**Runa Memory Access:**
- `buckets`: `memory_set_pointer(table, 0, buckets)` / `memory_get_pointer(table, 0)`
- `bucket_count`: `memory_set_integer(table, 8, bucket_count)` / `memory_get_integer(table, 8)`
- `entry_count`: `memory_set_integer(table, 16, entry_count)` / `memory_get_integer(table, 16)`
- `hash_func`: `memory_set_pointer(table, 24, hash_func)` / `memory_get_pointer(table, 24)`
- `compare_func`: `memory_set_pointer(table, 32, compare_func)` / `memory_get_pointer(table, 32)`
- `free_key`: `memory_set_pointer(table, 40, free_key)` / `memory_get_pointer(table, 40)`
- `free_value`: `memory_set_pointer(table, 48, free_value)` / `memory_get_pointer(table, 48)`

## Systematic Fix Strategy

### Phase 1: Audit Pattern
For each module, search for these incorrect patterns:

1. `memory_set_integer(obj, offset, pointer_value)` where the field is a pointer
2. `memory_get_integer(obj, offset)` where the field is a pointer
3. Incorrect structure sizes in `memory_allocate` calls
4. Incorrect field offsets in memory access

### Phase 2: Fix Pattern
Replace incorrect patterns with correct ones:

1. Pointer storage: `memory_set_integer` → `memory_set_pointer`
2. Pointer retrieval: `memory_get_integer` → `memory_get_pointer`
3. Verify structure sizes match C struct sizes (with padding)
4. Verify field offsets match C struct layouts (with padding)

### Phase 3: Validation
1. Compile each fixed module
2. Test basic functionality
3. Run comprehensive tests
4. Verify bootstrap compilation works

## Critical Files to Fix

1. **src/lexer.runa** - Token creation and lexer structure access
2. **src/parser.runa** - All AST node creation and access
3. **src/containers.runa** - Vector, list operations
4. **src/hashtable.runa** - Hash table operations
5. **src/string_utils.runa** - String utility structures
6. **src/codegen.runa** - AST traversal and code generation

This systematic approach will fix the foundational memory management issues preventing the compiler from functioning correctly.