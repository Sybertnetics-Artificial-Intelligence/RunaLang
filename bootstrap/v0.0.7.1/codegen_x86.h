#ifndef CODEGEN_X86_H
#define CODEGEN_X86_H

#include "parser.h"

typedef struct {
    char *name;
    int stack_offset;
    char *type_name; // Type of this variable (Integer or custom)
} Variable;

typedef struct {
    char *value;
    char *label;
} StringLiteral;

typedef struct {
    FILE *output_file;
    Variable *variables;      // Dynamic array
    int variable_count;
    int variable_capacity;    // Current capacity
    int stack_offset;
    int label_counter;
    StringLiteral *strings;   // Dynamic array
    int string_count;
    int string_capacity;      // Current capacity
    Program *current_program; // To access type definitions
} CodeGenerator;

CodeGenerator* codegen_create(const char *output_filename);
void codegen_destroy(CodeGenerator *codegen);
void codegen_generate(CodeGenerator *codegen, Program *program);

#endif