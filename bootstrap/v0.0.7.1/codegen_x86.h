/*
 * Copyright 2025 Sybertnetics Artificial Intelligence Solutions
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
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