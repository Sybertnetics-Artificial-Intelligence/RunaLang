# Structure Offset Reference for v0.0.7.5

## CodeGenerator Structure (64-bit system with padding)
```c
typedef struct {
    FILE *output_file;         // Offset 0  (8 bytes pointer)
    Variable *variables;       // Offset 8  (8 bytes pointer)
    int variable_count;        // Offset 16 (4 bytes)
    int variable_capacity;     // Offset 20 (4 bytes)
    int stack_offset;          // Offset 24 (4 bytes)
    int label_counter;         // Offset 28 (4 bytes)
    StringLiteral *strings;    // Offset 32 (8 bytes pointer - aligned to 8-byte boundary)
    int string_count;          // Offset 40 (4 bytes)
    int string_capacity;       // Offset 44 (4 bytes)
    Program *current_program;  // Offset 48 (8 bytes pointer - aligned to 8-byte boundary)
    LoopContext *loop_stack;   // Offset 56 (8 bytes pointer)
    int loop_depth;            // Offset 64 (4 bytes)
    int loop_capacity;         // Offset 68 (4 bytes)
} CodeGenerator;
```

## Function Structure
```c
typedef struct {
    char *name;                // Offset 0  (8 bytes pointer)
    Parameter *parameters;     // Offset 8  (8 bytes pointer)
    int parameter_count;       // Offset 16 (4 bytes)
    int padding;              // Offset 20 (4 bytes padding)
    char *return_type;         // Offset 24 (8 bytes pointer - aligned)
    Statement **statements;    // Offset 32 (8 bytes pointer)
    int statement_count;       // Offset 40 (4 bytes)
} Function;
```

## Parameter Structure
```c
typedef struct {
    char *name;     // Offset 0  (8 bytes pointer)
    char *type;     // Offset 8  (8 bytes pointer)
} Parameter;
sizeof(Parameter) = 16 bytes
```

## Variable Structure
```c
typedef struct {
    char *name;           // Offset 0  (8 bytes pointer)
    int stack_offset;     // Offset 8  (4 bytes)
    int padding;          // Offset 12 (4 bytes padding)
    char *type_name;      // Offset 16 (8 bytes pointer - aligned)
    int is_parameter;     // Offset 24 (4 bytes)
    int padding2;         // Offset 28 (4 bytes padding)
} Variable;
sizeof(Variable) = 32 bytes
```

## Access Rules for Runa Code

### For int fields (4 bytes):
- Use `memory_get_int32()` for reading
- Use `memory_set_int32()` for writing

### For pointer fields (8 bytes):
- Use `memory_get_integer()` for reading (Integer in Runa = pointer)
- Use `memory_set_integer()` for writing

### Correct CodeGenerator field access:
- output_file: offset 0, use memory_get/set_integer
- variables: offset 8, use memory_get/set_integer
- variable_count: offset 16, use memory_get/set_int32
- variable_capacity: offset 20, use memory_get/set_int32
- stack_offset: offset 24, use memory_get/set_int32
- label_counter: offset 28, use memory_get/set_int32
- strings: offset 32, use memory_get/set_integer
- string_count: offset 40, use memory_get/set_int32
- string_capacity: offset 44, use memory_get/set_int32
- current_program: offset 48, use memory_get/set_integer
- loop_stack: offset 56, use memory_get/set_integer
- loop_depth: offset 64, use memory_get/set_int32
- loop_capacity: offset 68, use memory_get/set_int32