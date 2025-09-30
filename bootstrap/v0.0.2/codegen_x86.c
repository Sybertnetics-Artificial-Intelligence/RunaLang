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
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "codegen_x86.h"

static char* string_duplicate(const char *str) {
    if (!str) return NULL;
    int len = strlen(str);
    char *dup = malloc(len + 1);
    strcpy(dup, str);
    return dup;
}

static int codegen_find_variable(CodeGenerator *codegen, const char *name) {
    for (int i = 0; i < codegen->variable_count; i++) {
        if (strcmp(codegen->variables[i].name, name) == 0) {
            return i;
        }
    }
    return -1;
}

static int codegen_add_variable(CodeGenerator *codegen, const char *name) {
    if (codegen->variable_count >= MAX_VARIABLES) {
        fprintf(stderr, "Codegen error: Too many variables\n");
        exit(1);
    }

    codegen->stack_offset += 8; // 8 bytes for each variable
    int var_index = codegen->variable_count;
    codegen->variables[var_index].name = string_duplicate(name);
    codegen->variables[var_index].stack_offset = codegen->stack_offset;
    codegen->variable_count++;

    return var_index;
}

static void codegen_generate_expression(CodeGenerator *codegen, Expression *expr) {
    switch (expr->type) {
        case EXPR_INTEGER:
            fprintf(codegen->output_file, "    movq $%d, %%rax\n", expr->data.integer_value);
            break;

        case EXPR_VARIABLE: {
            int var_index = codegen_find_variable(codegen, expr->data.variable_name);
            if (var_index == -1) {
                fprintf(stderr, "Codegen error: Unknown variable '%s'\n", expr->data.variable_name);
                exit(1);
            }
            int offset = codegen->variables[var_index].stack_offset;
            fprintf(codegen->output_file, "    movq -%d(%%rbp), %%rax\n", offset);
            break;
        }

        case EXPR_BINARY_OP:
            // Generate left operand (result in %rax)
            codegen_generate_expression(codegen, expr->data.binary_op.left);
            // Push left operand to stack
            fprintf(codegen->output_file, "    pushq %%rax\n");
            // Generate right operand (result in %rax)
            codegen_generate_expression(codegen, expr->data.binary_op.right);
            // Pop left operand from stack to %rbx
            fprintf(codegen->output_file, "    popq %%rbx\n");

            if (expr->data.binary_op.operator == TOKEN_PLUS) {
                fprintf(codegen->output_file, "    addq %%rbx, %%rax\n");
            } else if (expr->data.binary_op.operator == TOKEN_MINUS) {
                fprintf(codegen->output_file, "    subq %%rax, %%rbx\n");
                fprintf(codegen->output_file, "    movq %%rbx, %%rax\n");
            }
            break;

        case EXPR_COMPARISON:
            // Generate left operand (result in %rax)
            codegen_generate_expression(codegen, expr->data.comparison.left);
            // Push left operand to stack
            fprintf(codegen->output_file, "    pushq %%rax\n");
            // Generate right operand (result in %rax)
            codegen_generate_expression(codegen, expr->data.comparison.right);
            // Pop left operand from stack to %rbx
            fprintf(codegen->output_file, "    popq %%rbx\n");

            // Compare and set result (0 or 1)
            fprintf(codegen->output_file, "    cmpq %%rax, %%rbx\n");
            if (expr->data.comparison.comparison_op == TOKEN_EQUAL) {
                fprintf(codegen->output_file, "    sete %%al\n");
            } else if (expr->data.comparison.comparison_op == TOKEN_LESS) {
                fprintf(codegen->output_file, "    setl %%al\n");
            }
            fprintf(codegen->output_file, "    movzbq %%al, %%rax\n");
            break;
    }
}

static void codegen_generate_statement(CodeGenerator *codegen, Statement *stmt) {
    switch (stmt->type) {
        case STMT_LET: {
            // Add variable to symbol table
            codegen_add_variable(codegen, stmt->data.let_stmt.variable_name);

            // Generate expression (result in %rax)
            codegen_generate_expression(codegen, stmt->data.let_stmt.expression);

            // Store value in variable's stack slot
            int var_index = codegen_find_variable(codegen, stmt->data.let_stmt.variable_name);
            int offset = codegen->variables[var_index].stack_offset;
            fprintf(codegen->output_file, "    movq %%rax, -%d(%%rbp)\n", offset);
            break;
        }

        case STMT_SET: {
            // Generate expression (result in %rax)
            codegen_generate_expression(codegen, stmt->data.set_stmt.expression);

            // Store value in variable's stack slot
            int var_index = codegen_find_variable(codegen, stmt->data.set_stmt.variable_name);
            if (var_index == -1) {
                fprintf(stderr, "Codegen error: Unknown variable '%s'\n", stmt->data.set_stmt.variable_name);
                exit(1);
            }
            int offset = codegen->variables[var_index].stack_offset;
            fprintf(codegen->output_file, "    movq %%rax, -%d(%%rbp)\n", offset);
            break;
        }

        case STMT_RETURN:
            // Generate expression (result in %rax)
            codegen_generate_expression(codegen, stmt->data.return_stmt.expression);
            // Function epilogue
            fprintf(codegen->output_file, "    movq %%rbp, %%rsp\n");
            fprintf(codegen->output_file, "    popq %%rbp\n");
            fprintf(codegen->output_file, "    ret\n");
            break;

        case STMT_IF: {
            int label_num = codegen->label_counter++;
            int else_label = label_num * 10 + 1;
            int end_label = label_num * 10 + 2;

            // Generate condition (result in %rax)
            codegen_generate_expression(codegen, stmt->data.if_stmt.condition);
            // Test if condition is false (0)
            fprintf(codegen->output_file, "    testq %%rax, %%rax\n");
            fprintf(codegen->output_file, "    jz .L%d\n", else_label);

            // Generate if body
            for (int i = 0; i < stmt->data.if_stmt.if_body_count; i++) {
                codegen_generate_statement(codegen, stmt->data.if_stmt.if_body[i]);
            }
            fprintf(codegen->output_file, "    jmp .L%d\n", end_label);

            // Generate else body
            fprintf(codegen->output_file, ".L%d:\n", else_label);
            for (int i = 0; i < stmt->data.if_stmt.else_body_count; i++) {
                codegen_generate_statement(codegen, stmt->data.if_stmt.else_body[i]);
            }

            fprintf(codegen->output_file, ".L%d:\n", end_label);
            break;
        }

        case STMT_WHILE: {
            int label_num = codegen->label_counter++;
            int loop_start = label_num * 10 + 1;
            int loop_end = label_num * 10 + 2;

            // Loop start label
            fprintf(codegen->output_file, ".L%d:\n", loop_start);

            // Generate condition (result in %rax)
            codegen_generate_expression(codegen, stmt->data.while_stmt.condition);
            // Test if condition is false (0)
            fprintf(codegen->output_file, "    testq %%rax, %%rax\n");
            fprintf(codegen->output_file, "    jz .L%d\n", loop_end);

            // Generate loop body
            for (int i = 0; i < stmt->data.while_stmt.body_count; i++) {
                codegen_generate_statement(codegen, stmt->data.while_stmt.body[i]);
            }

            // Jump back to loop start
            fprintf(codegen->output_file, "    jmp .L%d\n", loop_start);

            // Loop end label
            fprintf(codegen->output_file, ".L%d:\n", loop_end);
            break;
        }
    }
}

CodeGenerator* codegen_create(const char *output_filename) {
    CodeGenerator *codegen = malloc(sizeof(CodeGenerator));
    codegen->output_file = fopen(output_filename, "w");
    codegen->variable_count = 0;
    codegen->stack_offset = 0;
    codegen->label_counter = 0;

    if (!codegen->output_file) {
        fprintf(stderr, "Error: Could not open output file '%s'\n", output_filename);
        free(codegen);
        return NULL;
    }

    return codegen;
}

void codegen_destroy(CodeGenerator *codegen) {
    if (codegen) {
        if (codegen->output_file) {
            fclose(codegen->output_file);
        }
        for (int i = 0; i < codegen->variable_count; i++) {
            free(codegen->variables[i].name);
        }
        free(codegen);
    }
}

void codegen_generate(CodeGenerator *codegen, Program *program) {
    fprintf(codegen->output_file, ".text\n");
    fprintf(codegen->output_file, ".globl main\n");
    fprintf(codegen->output_file, "\n");
    fprintf(codegen->output_file, "main:\n");

    // Function prologue
    fprintf(codegen->output_file, "    pushq %%rbp\n");
    fprintf(codegen->output_file, "    movq %%rsp, %%rbp\n");

    // Reserve stack space for variables (will be calculated after processing all variables)
    int stack_reservation_pos = ftell(codegen->output_file);
    fprintf(codegen->output_file, "                              \n"); // Placeholder

    // Generate statements
    for (int i = 0; i < program->statement_count; i++) {
        codegen_generate_statement(codegen, program->statements[i]);
    }

    // Go back and fill in stack space reservation
    long current_pos = ftell(codegen->output_file);
    fseek(codegen->output_file, stack_reservation_pos, SEEK_SET);
    if (codegen->stack_offset > 0) {
        fprintf(codegen->output_file, "    subq $%d, %%rsp\n", (codegen->stack_offset + 15) & ~15); // Align to 16 bytes
    }
    fseek(codegen->output_file, current_pos, SEEK_SET);
}