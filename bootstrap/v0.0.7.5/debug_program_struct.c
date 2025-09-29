#include <stdio.h>
#include <stddef.h>

// Copy the exact structs from v0.0.7.3 parser.h

typedef struct GlobalVariable {
    char *name;
    char *type;
    void *initial_value;  // Expression pointer
} GlobalVariable;

typedef struct {
    void **functions;        // Function **functions
    int function_count;      // int function_count
    int function_capacity;   // int function_capacity
    void **types;           // TypeDefinition **types
    int type_count;         // int type_count
    int type_capacity;      // int type_capacity
    void **imports;         // Import **imports
    int import_count;       // int import_count
    int import_capacity;    // int import_capacity
    GlobalVariable **globals;  // GlobalVariable **globals
    int global_count;       // int global_count
    int global_capacity;    // int global_capacity
} Program;

int main() {
    printf("=== PROGRAM STRUCT GROUND TRUTH ===\n");
    printf("sizeof(Program) = %zu\n", sizeof(Program));
    printf("sizeof(GlobalVariable) = %zu\n", sizeof(GlobalVariable));
    printf("sizeof(void*) = %zu\n", sizeof(void*));
    printf("sizeof(int) = %zu\n", sizeof(int));
    printf("\n=== PROGRAM FIELD OFFSETS ===\n");
    printf("functions offset = %zu\n", offsetof(Program, functions));
    printf("function_count offset = %zu\n", offsetof(Program, function_count));
    printf("function_capacity offset = %zu\n", offsetof(Program, function_capacity));
    printf("types offset = %zu\n", offsetof(Program, types));
    printf("type_count offset = %zu\n", offsetof(Program, type_count));
    printf("type_capacity offset = %zu\n", offsetof(Program, type_capacity));
    printf("imports offset = %zu\n", offsetof(Program, imports));
    printf("import_count offset = %zu\n", offsetof(Program, import_count));
    printf("import_capacity offset = %zu\n", offsetof(Program, import_capacity));
    printf("globals offset = %zu\n", offsetof(Program, globals));
    printf("global_count offset = %zu\n", offsetof(Program, global_count));
    printf("global_capacity offset = %zu\n", offsetof(Program, global_capacity));
    printf("\n=== GLOBALVARIABLE FIELD OFFSETS ===\n");
    printf("name offset = %zu\n", offsetof(GlobalVariable, name));
    printf("type offset = %zu\n", offsetof(GlobalVariable, type));
    printf("initial_value offset = %zu\n", offsetof(GlobalVariable, initial_value));

    return 0;
}