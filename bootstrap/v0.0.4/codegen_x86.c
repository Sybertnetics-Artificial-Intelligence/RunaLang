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

static int codegen_add_string_literal(CodeGenerator *codegen, const char *value) {
    if (codegen->string_count >= MAX_STRINGS) {
        fprintf(stderr, "Codegen error: Too many string literals\n");
        exit(1);
    }

    int str_index = codegen->string_count;
    codegen->strings[str_index].value = string_duplicate(value);

    // Generate unique label for this string
    int label_len = snprintf(NULL, 0, ".STR%d", str_index) + 1;
    codegen->strings[str_index].label = malloc(label_len);
    snprintf(codegen->strings[str_index].label, label_len, ".STR%d", str_index);

    codegen->string_count++;
    return str_index;
}

static void codegen_collect_strings_from_expression(CodeGenerator *codegen, Expression *expr) {
    if (!expr) return;

    switch (expr->type) {
        case EXPR_STRING_LITERAL:
            // Check if string already exists
            for (int i = 0; i < codegen->string_count; i++) {
                if (strcmp(codegen->strings[i].value, expr->data.string_literal) == 0) {
                    return; // Already added
                }
            }
            codegen_add_string_literal(codegen, expr->data.string_literal);
            break;

        case EXPR_BINARY_OP:
            codegen_collect_strings_from_expression(codegen, expr->data.binary_op.left);
            codegen_collect_strings_from_expression(codegen, expr->data.binary_op.right);
            break;

        case EXPR_COMPARISON:
            codegen_collect_strings_from_expression(codegen, expr->data.comparison.left);
            codegen_collect_strings_from_expression(codegen, expr->data.comparison.right);
            break;

        case EXPR_FUNCTION_CALL:
            for (int i = 0; i < expr->data.function_call.argument_count; i++) {
                codegen_collect_strings_from_expression(codegen, expr->data.function_call.arguments[i]);
            }
            break;

        case EXPR_INTEGER:
        case EXPR_VARIABLE:
            // No strings to collect
            break;
    }
}

static void codegen_collect_strings_from_statement(CodeGenerator *codegen, Statement *stmt) {
    if (!stmt) return;

    switch (stmt->type) {
        case STMT_LET:
            codegen_collect_strings_from_expression(codegen, stmt->data.let_stmt.expression);
            break;

        case STMT_SET:
            codegen_collect_strings_from_expression(codegen, stmt->data.set_stmt.expression);
            break;

        case STMT_RETURN:
            codegen_collect_strings_from_expression(codegen, stmt->data.return_stmt.expression);
            break;

        case STMT_PRINT:
            codegen_collect_strings_from_expression(codegen, stmt->data.print_stmt.expression);
            break;

        case STMT_IF:
            codegen_collect_strings_from_expression(codegen, stmt->data.if_stmt.condition);
            for (int i = 0; i < stmt->data.if_stmt.if_body_count; i++) {
                codegen_collect_strings_from_statement(codegen, stmt->data.if_stmt.if_body[i]);
            }
            for (int i = 0; i < stmt->data.if_stmt.else_body_count; i++) {
                codegen_collect_strings_from_statement(codegen, stmt->data.if_stmt.else_body[i]);
            }
            break;

        case STMT_WHILE:
            codegen_collect_strings_from_expression(codegen, stmt->data.while_stmt.condition);
            for (int i = 0; i < stmt->data.while_stmt.body_count; i++) {
                codegen_collect_strings_from_statement(codegen, stmt->data.while_stmt.body[i]);
            }
            break;
    }
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
            } else if (expr->data.binary_op.operator == TOKEN_MULTIPLIED) {
                fprintf(codegen->output_file, "    imulq %%rbx, %%rax\n");
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

        case EXPR_FUNCTION_CALL:
            // System V ABI: first argument goes in %rdi
            if (expr->data.function_call.argument_count > 0) {
                codegen_generate_expression(codegen, expr->data.function_call.arguments[0]);
                fprintf(codegen->output_file, "    movq %%rax, %%rdi\n");
            }

            // Call the function
            fprintf(codegen->output_file, "    call %s\n", expr->data.function_call.function_name);
            // Result is already in %rax
            break;

        case EXPR_STRING_LITERAL: {
            // Add string to string literals table if not already present
            int str_index = -1;
            for (int i = 0; i < codegen->string_count; i++) {
                if (strcmp(codegen->strings[i].value, expr->data.string_literal) == 0) {
                    str_index = i;
                    break;
                }
            }
            if (str_index == -1) {
                str_index = codegen_add_string_literal(codegen, expr->data.string_literal);
            }

            // Load address of string literal into %rax
            fprintf(codegen->output_file, "    leaq %s(%%rip), %%rax\n", codegen->strings[str_index].label);
            break;
        }
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

        case STMT_PRINT: {
            // Generate expression (string address in %rax)
            codegen_generate_expression(codegen, stmt->data.print_stmt.expression);

            // Call print function with string address in %rdi
            fprintf(codegen->output_file, "    movq %%rax, %%rdi\n");
            fprintf(codegen->output_file, "    call print_string\n");
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
    codegen->string_count = 0;

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
        for (int i = 0; i < codegen->string_count; i++) {
            free(codegen->strings[i].value);
            free(codegen->strings[i].label);
        }
        free(codegen);
    }
}

static void codegen_generate_function(CodeGenerator *codegen, Function *func) {
    // Reset variable state for each function
    codegen->variable_count = 0;
    codegen->stack_offset = 0;

    // Function label
    fprintf(codegen->output_file, "%s:\n", func->name);

    // Function prologue
    fprintf(codegen->output_file, "    pushq %%rbp\n");
    fprintf(codegen->output_file, "    movq %%rsp, %%rbp\n");

    // Handle parameters (System V ABI: first parameter in %rdi)
    if (func->parameter_count > 0) {
        // Add parameter as a variable and store from %rdi
        int param_index = codegen_add_variable(codegen, func->parameters[0].name);
        int param_offset = codegen->variables[param_index].stack_offset;
        fprintf(codegen->output_file, "    movq %%rdi, -%d(%%rbp)\n", param_offset);
    }

    // Reserve stack space for variables (will be calculated after processing all variables)
    long stack_reservation_pos = ftell(codegen->output_file);
    fprintf(codegen->output_file, "                              \n"); // Placeholder

    // Generate function body statements
    for (int i = 0; i < func->statement_count; i++) {
        codegen_generate_statement(codegen, func->statements[i]);
    }

    // Go back and fill in stack space reservation
    long current_pos = ftell(codegen->output_file);
    fseek(codegen->output_file, stack_reservation_pos, SEEK_SET);
    if (codegen->stack_offset > 0) {
        fprintf(codegen->output_file, "    subq $%d, %%rsp\n", (codegen->stack_offset + 15) & ~15); // Align to 16 bytes
    }
    fseek(codegen->output_file, current_pos, SEEK_SET);
}

void codegen_generate(CodeGenerator *codegen, Program *program) {
    // First pass: collect all string literals by analyzing the AST
    for (int i = 0; i < program->function_count; i++) {
        Function *func = program->functions[i];
        for (int j = 0; j < func->statement_count; j++) {
            codegen_collect_strings_from_statement(codegen, func->statements[j]);
        }
    }

    // Generate .rodata section with string literals
    if (codegen->string_count > 0) {
        fprintf(codegen->output_file, ".section .rodata\n");
        for (int i = 0; i < codegen->string_count; i++) {
            fprintf(codegen->output_file, "%s:\n", codegen->strings[i].label);
            fprintf(codegen->output_file, "    .string \"%s\"\n", codegen->strings[i].value);
        }
        fprintf(codegen->output_file, "\n");
    }

    // Generate .text section
    fprintf(codegen->output_file, ".text\n");

    // Add print_string runtime function
    fprintf(codegen->output_file, "print_string:\n");
    fprintf(codegen->output_file, "    pushq %%rbp\n");
    fprintf(codegen->output_file, "    movq %%rsp, %%rbp\n");
    fprintf(codegen->output_file, "    \n");
    fprintf(codegen->output_file, "    # Calculate string length\n");
    fprintf(codegen->output_file, "    movq %%rdi, %%rsi  # Save string pointer\n");
    fprintf(codegen->output_file, "    movq %%rdi, %%rcx  # Counter for strlen\n");
    fprintf(codegen->output_file, "    xorq %%rax, %%rax  # Length accumulator\n");
    fprintf(codegen->output_file, ".strlen_loop:\n");
    fprintf(codegen->output_file, "    cmpb $0, (%%rcx)\n");
    fprintf(codegen->output_file, "    je .strlen_done\n");
    fprintf(codegen->output_file, "    incq %%rcx\n");
    fprintf(codegen->output_file, "    incq %%rax\n");
    fprintf(codegen->output_file, "    jmp .strlen_loop\n");
    fprintf(codegen->output_file, ".strlen_done:\n");
    fprintf(codegen->output_file, "    \n");
    fprintf(codegen->output_file, "    # Call write syscall (sys_write = 1)\n");
    fprintf(codegen->output_file, "    movq $1, %%rdi     # fd = stdout\n");
    fprintf(codegen->output_file, "    movq %%rsi, %%rsi   # buf = string pointer (already in rsi)\n");
    fprintf(codegen->output_file, "    movq %%rax, %%rdx   # count = string length\n");
    fprintf(codegen->output_file, "    movq $1, %%rax     # syscall number for write\n");
    fprintf(codegen->output_file, "    syscall\n");
    fprintf(codegen->output_file, "    \n");
    fprintf(codegen->output_file, "    # Print newline\n");
    fprintf(codegen->output_file, "    movq $1, %%rdi     # fd = stdout\n");
    fprintf(codegen->output_file, "    leaq .newline(%%rip), %%rsi  # newline string\n");
    fprintf(codegen->output_file, "    movq $1, %%rdx     # count = 1\n");
    fprintf(codegen->output_file, "    movq $1, %%rax     # syscall number for write\n");
    fprintf(codegen->output_file, "    syscall\n");
    fprintf(codegen->output_file, "    \n");
    fprintf(codegen->output_file, "    popq %%rbp\n");
    fprintf(codegen->output_file, "    ret\n");
    fprintf(codegen->output_file, "\n");
    fprintf(codegen->output_file, ".section .rodata\n");
    fprintf(codegen->output_file, ".newline:\n");
    fprintf(codegen->output_file, "    .string \"\\n\"\n");
    fprintf(codegen->output_file, "\n");
    fprintf(codegen->output_file, ".text\n");

    // Generate all functions
    for (int i = 0; i < program->function_count; i++) {
        Function *func = program->functions[i];

        // Make main function global
        if (strcmp(func->name, "main") == 0) {
            fprintf(codegen->output_file, ".globl main\n");
        }

        fprintf(codegen->output_file, "\n");
        codegen_generate_function(codegen, func);
    }
}