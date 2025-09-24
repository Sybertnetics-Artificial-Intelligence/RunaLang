#ifndef CODEGEN_X86_H
#define CODEGEN_X86_H

#include "parser.h"

#define MAX_VARIABLES 64
#define MAX_STRINGS 32

typedef struct {
    char *name;
    int stack_offset;
} Variable;

typedef struct {
    char *value;
    char *label;
} StringLiteral;

typedef struct {
    FILE *output_file;
    Variable variables[MAX_VARIABLES];
    int variable_count;
    int stack_offset;
    int label_counter;
    StringLiteral strings[MAX_STRINGS];
    int string_count;
} CodeGenerator;

CodeGenerator* codegen_create(const char *output_filename);
void codegen_destroy(CodeGenerator *codegen);
void codegen_generate(CodeGenerator *codegen, Program *program);

#endif