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
# API Mapping: C to Runa Transliteration

## **Overview**

This document provides the comprehensive mapping from C functions and patterns to their Runa equivalents during the v0.0.7.3 → v0.0.7.5 transliteration process. This ensures consistency and correctness in the translation.

## **Memory Management**

### **C Patterns** → **Runa Patterns**

```c
// C: Manual memory management
char* ptr = malloc(size);
free(ptr);
```

```runa
# Runa: System allocation functions
Let ptr be allocate(size)
deallocate(ptr)
```

### **Memory Functions**
| C Function | Runa Function | Notes |
|------------|---------------|-------|
| `malloc(size)` | `allocate(size)` | Direct mapping to system function |
| `free(ptr)` | `deallocate(ptr)` | Direct mapping to system function |
| `calloc(n, size)` | `allocate(n * size)` + zero | Manual zeroing required |
| `realloc(ptr, size)` | Manual implementation | Allocate new, copy, deallocate old |

## **String Handling**

### **C Patterns** → **Runa Patterns**

```c
// C: String operations
strlen(str);
strcpy(dest, src);
strcat(dest, src);
strcmp(str1, str2);
```

```runa
# Runa: Built-in string functions
string_length(str)
# Manual copy or string_concat for concatenation
string_concat(str1, str2)
string_compare(str1, str2)
```

### **String Functions**
| C Function | Runa Function | Notes |
|------------|---------------|-------|
| `strlen(str)` | `string_length(str)` | Built-in function |
| `strcpy(dest, src)` | `Set dest to src` | Assignment in Runa |
| `strcat(dest, src)` | `string_concat(dest, src)` | Built-in function |
| `strcmp(str1, str2)` | `string_compare(str1, str2)` | Built-in function |
| `strncmp(s1, s2, n)` | `string_compare(string_substring(s1, 0, n), string_substring(s2, 0, n))` | Composite operation |

## **Data Structure Patterns**

### **C Struct** → **Runa Type**

```c
// C: Structure definition
typedef struct {
    int x;
    char* name;
} Point;
```

```runa
# Runa: Type definition
Type called "Point":
    x as Integer,
    name as String
End Type
```

### **Function Definitions**

```c
// C: Function definition
int add_numbers(int a, int b) {
    return a + b;
}
```

```runa
# Runa: Process definition
Process called "add_numbers" takes a as Integer, b as Integer returns Integer:
    Return a plus b
End Process
```

## **Control Flow Mapping**

### **Conditional Statements**

```c
// C: if-else
if (condition) {
    // statements
} else if (other_condition) {
    // statements
} else {
    // statements
}
```

```runa
# Runa: If-Otherwise
If condition:
    # statements
Otherwise If other_condition:
    # statements
Otherwise:
    # statements
End If
```

### **Loop Statements**

```c
// C: while loop
while (condition) {
    if (break_condition) break;
    if (continue_condition) continue;
    // statements
}
```

```runa
# Runa: While loop
While condition:
    If break_condition:
        Break
    End If
    If continue_condition:
        Continue
    End If
    # statements
End While
```

## **Error Handling Patterns**

### **C Patterns** → **Runa Patterns**

```c
// C: Error checking
if (!ptr) {
    fprintf(stderr, "Error message\n");
    return -1;
}
assert(condition);
exit(1);
```

```runa
# Runa: Error handling
If ptr is equal to 0:
    panic("Error message")
End If
assert(condition)
exit_with_code(1)
```

## **File I/O Mapping**

### **Basic File Operations**

```c
// C: File operations
FILE* file = fopen(filename, "r");
char* content = read_entire_file(filename);
fclose(file);
```

```runa
# Runa: File operations
Let handle be file_open(filename, "r")
Let content be read_file(filename)
file_close(handle)
```

### **File Functions**
| C Function | Runa Function | Notes |
|------------|---------------|-------|
| `fopen(name, mode)` | `file_open(name, mode)` | Built-in function |
| `fclose(handle)` | `file_close(handle)` | Built-in function |
| `fread(buf, size, count, file)` | `file_read_line(handle)` | Line-based reading |
| `fwrite(buf, size, count, file)` | `file_write_line(handle, content)` | Line-based writing |
| Custom `read_file()` | `read_file(filename)` | Built-in convenience function |

## **Lexer-Specific Mappings**

### **Token Structure**

```c
// C: Token structure
typedef struct {
    TokenType type;
    char* value;
    int line;
    int column;
} Token;
```

```runa
# Runa: Token type
Type called "Token":
    token_type as Integer,
    value as String,
    line as Integer,
    column as Integer
End Type
```

### **Lexer Functions**
| C Function | Runa Function | Purpose |
|------------|---------------|---------|
| `lexer_create(source)` | `lexer_create(source)` | Initialize lexer |
| `lexer_next_token(lexer)` | `lexer_next_token(lexer)` | Get next token |
| `lexer_advance(lexer)` | `lexer_advance(lexer)` | Advance position |
| `is_alpha(ch)` | `is_alpha(ch)` | Character classification |
| `is_digit(ch)` | `is_digit(ch)` | Character classification |

## **Parser-Specific Mappings**

### **AST Node Types**

```c
// C: Expression types
typedef enum {
    EXPR_INTEGER,
    EXPR_VARIABLE,
    EXPR_BINARY_OP
} ExpressionType;
```

```runa
# Runa: Expression type enumeration
# Will be handled as Integer constants
Let EXPR_INTEGER be 0
Let EXPR_VARIABLE be 1
Let EXPR_BINARY_OP be 2
```

### **Parser Functions**
| C Function | Runa Function | Purpose |
|------------|---------------|---------|
| `parser_create(lexer)` | `parser_create(lexer)` | Initialize parser |
| `parse_expression(parser)` | `parse_expression(parser)` | Parse expression |
| `parse_statement(parser)` | `parse_statement(parser)` | Parse statement |
| `expect_token(parser, type)` | `expect_token(parser, type)` | Token validation |

## **Code Generator Mappings**

### **Assembly Generation**

```c
// C: Assembly output
fprintf(output, "\tmovq $%d, %%rax\n", value);
fprintf(output, "\tret\n");
```

```runa
# Runa: Assembly output using string functions
Let instruction be string_concat("\tmovq $", integer_to_string(value))
Set instruction to string_concat(instruction, ", %rax\n")
write_file(output_file, instruction)
write_file(output_file, "\tret\n")
```

### **Code Generation Functions**
| C Function | Runa Function | Purpose |
|------------|---------------|---------|
| `codegen_create(filename)` | `codegen_create(filename)` | Initialize codegen |
| `emit_instruction(gen, instr)` | `emit_instruction(gen, instr)` | Output assembly |
| `allocate_register(gen)` | `allocate_register(gen)` | Register allocation |
| `generate_expression(gen, expr)` | `generate_expression(gen, expr)` | Expression codegen |

## **Container Mappings**

### **Dynamic Arrays**

```c
// C: Dynamic array management
typedef struct {
    void** items;
    size_t count;
    size_t capacity;
} Array;
```

```runa
# Runa: Array type
Type called "Array":
    items as Integer,  # Will hold pointer value
    count as Integer,
    capacity as Integer
End Type
```

### **Container Functions**
| C Function | Runa Function | Purpose |
|------------|---------------|---------|
| `array_create()` | `array_create()` | Initialize array |
| `array_append(arr, item)` | `array_append(arr, item)` | Add item |
| `array_get(arr, index)` | `array_get(arr, index)` | Get item |
| `array_destroy(arr)` | `array_destroy(arr)` | Cleanup array |

## **Hash Table Mappings**

### **Hash Table Structure**

```c
// C: Hash table
typedef struct {
    HashEntry** buckets;
    size_t size;
    size_t count;
} HashTable;
```

```runa
# Runa: Hash table type
Type called "HashTable":
    buckets as Integer,  # Pointer to buckets
    size as Integer,
    count as Integer
End Type
```

## **Runtime Integration**

### **C Runtime Functions** (Remain as C)
These functions are **NOT transliterated** - they remain as C and are called from Runa:

| Function Category | C Files | Runa Usage |
|-------------------|---------|------------|
| String operations | `runtime_string.c/h` | Call from Runa via built-ins |
| List operations | `runtime_list.c/h` | Call from Runa via built-ins |
| File I/O | `runtime_io.c/h` | Call from Runa via built-ins |
| Math functions | `runtime_math.c/h` | Call from Runa via built-ins |
| System functions | `runtime_system.c/h` | Call from Runa via built-ins |

## **Type Mappings**

### **Basic Types**
| C Type | Runa Type | Notes |
|--------|-----------|-------|
| `int` | `Integer` | 64-bit signed integer |
| `char*` | `String` | UTF-8 string |
| `char` | `Character` | Single character |
| `void*` | `Integer` | Pointer as integer value |
| `size_t` | `Integer` | Size as integer |
| `FILE*` | `Integer` | File handle as integer |

### **Pointer Handling**
```c
// C: Pointer operations
Node* node = malloc(sizeof(Node));
node->field = value;
```

```runa
# Runa: Simulated pointer operations
Let node be allocate(node_size)
# Field access requires offset calculation
Set field_value to get_field(node, field_offset)
set_field(node, field_offset, value)
```

## **Compilation Flags**

### **Debug Information**
```c
// C: Conditional compilation
#ifdef DEBUG
    printf("Debug: %s\n", message);
#endif
```

```runa
# Runa: Runtime debugging (simplified)
# Debug output handled through Print statements
If debug_enabled is equal to 1:
    Print message
End If
```

---

**This mapping document will be updated as transliteration progresses and new patterns are discovered.**