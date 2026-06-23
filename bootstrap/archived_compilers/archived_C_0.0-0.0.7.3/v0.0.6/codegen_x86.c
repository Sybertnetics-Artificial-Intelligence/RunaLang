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

// Calculate size of a type in bytes (codegen version)
static int codegen_calculate_type_size(const char *type_name, Program *program) {
    // Built-in types
    if (strcmp(type_name, "Integer") == 0) {
        return 8; // 64-bit integer
    }
    if (strcmp(type_name, "Byte") == 0) {
        return 1; // 8-bit byte
    }
    if (strcmp(type_name, "Short") == 0) {
        return 2; // 16-bit short
    }
    if (strcmp(type_name, "Long") == 0) {
        return 8; // 64-bit long
    }

    // Custom types - look up in the program
    if (program) {
        for (int i = 0; i < program->type_count; i++) {
            if (strcmp(program->types[i]->name, type_name) == 0) {
                return program->types[i]->size;
            }
        }
    }

    // Unknown type - default to 8 bytes
    return 8;
}

static int codegen_add_variable_with_type(CodeGenerator *codegen, const char *name, const char *type_name);

static int codegen_add_variable(CodeGenerator *codegen, const char *name) {
    return codegen_add_variable_with_type(codegen, name, "Integer");
}

static int codegen_add_variable_with_type(CodeGenerator *codegen, const char *name, const char *type_name) {
    // Grow array if needed
    if (codegen->variable_count >= codegen->variable_capacity) {
        codegen->variable_capacity *= 2;
        codegen->variables = realloc(codegen->variables,
                                     sizeof(Variable) * codegen->variable_capacity);
        if (!codegen->variables) {
            fprintf(stderr, "[CODEGEN ERROR] Out of memory allocating variables\n");
            exit(1);
        }
    }

    // Calculate size based on type
    int size = codegen_calculate_type_size(type_name ? type_name : "Integer", codegen->current_program);

    codegen->stack_offset += size;
    int var_index = codegen->variable_count;
    codegen->variables[var_index].name = string_duplicate(name);
    codegen->variables[var_index].stack_offset = codegen->stack_offset;
    codegen->variables[var_index].type_name = string_duplicate(type_name);
    codegen->variable_count++;

    return var_index;
}

static int codegen_add_string_literal(CodeGenerator *codegen, const char *value) {
    // Grow array if needed
    if (codegen->string_count >= codegen->string_capacity) {
        codegen->string_capacity *= 2;
        codegen->strings = realloc(codegen->strings,
                                   sizeof(StringLiteral) * codegen->string_capacity);
        if (!codegen->strings) {
            fprintf(stderr, "[CODEGEN ERROR] Out of memory allocating strings\n");
            exit(1);
        }
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
        case EXPR_TYPE_NAME:
            // No strings to collect
            break;

        case EXPR_FIELD_ACCESS:
            codegen_collect_strings_from_expression(codegen, expr->data.field_access.object);
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

        case STMT_EXPRESSION:
            codegen_collect_strings_from_expression(codegen, stmt->data.expr_stmt.expression);
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
                fprintf(stderr, "[CODEGEN ERROR] Unknown variable '%s'\n", expr->data.variable_name);
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
            } else if (expr->data.binary_op.operator == TOKEN_DIVIDED) {
                // Division: dividend in %rax, divisor in %rbx
                // Move divisor to %rcx to preserve %rbx
                fprintf(codegen->output_file, "    movq %%rax, %%rcx\n");  // Save divisor in %rcx
                fprintf(codegen->output_file, "    movq %%rbx, %%rax\n");  // Move dividend to %rax

                // Check for divide by zero
                fprintf(codegen->output_file, "    testq %%rcx, %%rcx\n");
                fprintf(codegen->output_file, "    jz .Ldiv_by_zero_%d\n", codegen->label_counter);

                // Sign extend %rax to %rdx:%rax
                fprintf(codegen->output_file, "    cqto\n");
                // Divide by %rcx, quotient in %rax, remainder in %rdx
                fprintf(codegen->output_file, "    idivq %%rcx\n");
                fprintf(codegen->output_file, "    jmp .Ldiv_done_%d\n", codegen->label_counter);

                // Divide by zero handler - return 0
                fprintf(codegen->output_file, ".Ldiv_by_zero_%d:\n", codegen->label_counter);
                fprintf(codegen->output_file, "    movq $0, %%rax\n");
                fprintf(codegen->output_file, ".Ldiv_done_%d:\n", codegen->label_counter);
                codegen->label_counter++;
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

        case EXPR_FUNCTION_CALL: {
            // Check if this is a list runtime function
            const char* func_name = expr->data.function_call.function_name;
            int is_list_function = (strcmp(func_name, "list_create") == 0 ||
                                    strcmp(func_name, "list_append") == 0 ||
                                    strcmp(func_name, "list_get") == 0 ||
                                    strcmp(func_name, "list_get_integer") == 0 ||
                                    strcmp(func_name, "list_length") == 0 ||
                                    strcmp(func_name, "list_destroy") == 0);

            // System V ABI: arguments go in %rdi, %rsi, %rdx, %rcx, %r8, %r9
            const char *arg_registers[] = {"%rdi", "%rsi", "%rdx", "%rcx", "%r8", "%r9"};
            int max_register_args = sizeof(arg_registers) / sizeof(arg_registers[0]);

            int arg_count = expr->data.function_call.argument_count;
            int register_arg_count = arg_count < max_register_args ? arg_count : max_register_args;

            // Evaluate arguments in reverse order and push them to stack to preserve order
            for (int i = register_arg_count - 1; i >= 0; i--) {
                codegen_generate_expression(codegen, expr->data.function_call.arguments[i]);
                fprintf(codegen->output_file, "    pushq %%rax\n");
            }

            // Pop arguments into correct registers
            for (int i = 0; i < register_arg_count; i++) {
                fprintf(codegen->output_file, "    popq %s\n", arg_registers[i]);
            }

            // Handle arguments beyond 6 (push to stack) - not fully implemented
            if (arg_count > max_register_args) {
                fprintf(stderr, "[CODEGEN WARNING] Functions with more than 6 arguments not fully supported yet\n");
            }

            // Call the function
            if (is_list_function) {
                // For list runtime functions, call the C function directly
                fprintf(codegen->output_file, "    call %s@PLT\n", func_name);
            } else {
                // For user-defined functions
                fprintf(codegen->output_file, "    call %s\n", func_name);
            }
            // Result is already in %rax
            break;
        }

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

        case EXPR_FIELD_ACCESS: {
            // For field access, we need the address of the struct
            Expression *obj = expr->data.field_access.object;

            // If the object is a variable, load its address
            if (obj->type == EXPR_VARIABLE) {
                int var_index = codegen_find_variable(codegen, obj->data.variable_name);
                if (var_index == -1) {
                    fprintf(stderr, "[CODEGEN ERROR] Unknown variable '%s'\n", obj->data.variable_name);
                    exit(1);
                }

                // Load the address of the struct
                int offset = codegen->variables[var_index].stack_offset;
                fprintf(codegen->output_file, "    leaq -%d(%%rbp), %%rax\n", offset);

                // Find the field offset based on the variable's type
                char *type_name = codegen->variables[var_index].type_name;
                if (!type_name) {
                    fprintf(stderr, "[CODEGEN ERROR] Variable '%s' has no type\n", obj->data.variable_name);
                    exit(1);
                }

                TypeDefinition *type = NULL;
                for (int i = 0; i < codegen->current_program->type_count; i++) {
                    if (strcmp(codegen->current_program->types[i]->name, type_name) == 0) {
                        type = codegen->current_program->types[i];
                        break;
                    }
                }

                if (!type) {
                    fprintf(stderr, "[CODEGEN ERROR] Unknown type '%s' (line %d)\n", type_name, __LINE__);
                    exit(1);
                }

                int field_offset = -1;
                for (int i = 0; i < type->field_count; i++) {
                    if (strcmp(type->fields[i].name, expr->data.field_access.field_name) == 0) {
                        field_offset = type->fields[i].offset;
                        break;
                    }
                }

                if (field_offset == -1) {
                    fprintf(stderr, "[CODEGEN ERROR] Type '%s' has no field '%s'\n", type_name, expr->data.field_access.field_name);
                    exit(1);
                }

                // Load the field value
                fprintf(codegen->output_file, "    movq %d(%%rax), %%rax\n", field_offset);
            } else {
                // Complex field access expressions not yet supported
                fprintf(stderr, "[CODEGEN ERROR] Complex field access expressions not implemented\n");
                exit(1);
            }
            break;
        }

        case EXPR_TYPE_NAME:
            // Type names don't generate code directly - they're handled in LET statements
            // This shouldn't be reached in normal execution
            fprintf(stderr, "[CODEGEN ERROR] Type names should only appear in LET statements\n");
            exit(1);
            break;
    }
}

static void codegen_generate_statement(CodeGenerator *codegen, Statement *stmt) {
    switch (stmt->type) {
        case STMT_LET: {
            // Check if this is a type allocation
            Expression *expr = stmt->data.let_stmt.expression;
            if (expr && expr->type == EXPR_TYPE_NAME) {
                // This is a struct allocation - find the type
                TypeDefinition *type = NULL;
                for (int i = 0; i < codegen->current_program->type_count; i++) {
                    if (strcmp(codegen->current_program->types[i]->name, expr->data.type_name) == 0) {
                        type = codegen->current_program->types[i];
                        break;
                    }
                }

                if (!type) {
                    fprintf(stderr, "[CODEGEN ERROR] Unknown type '%s' (line %d)\n", expr->data.type_name, __LINE__);
                    exit(1);
                }

                // Add variable with type information
                codegen_add_variable_with_type(codegen, stmt->data.let_stmt.variable_name, expr->data.type_name);

                // Zero-initialize the struct
                int var_index = codegen_find_variable(codegen, stmt->data.let_stmt.variable_name);
                int offset = codegen->variables[var_index].stack_offset;

                // Zero out the struct memory
                for (int i = 0; i < type->size; i += 8) {
                    fprintf(codegen->output_file, "    movq $0, -%d(%%rbp)\n", offset - i);
                }
            } else {
                // Regular expression - add variable to symbol table
                codegen_add_variable(codegen, stmt->data.let_stmt.variable_name);

                // Generate expression (result in %rax)
                codegen_generate_expression(codegen, stmt->data.let_stmt.expression);

                // Store value in variable's stack slot
                int var_index = codegen_find_variable(codegen, stmt->data.let_stmt.variable_name);
                int offset = codegen->variables[var_index].stack_offset;
                fprintf(codegen->output_file, "    movq %%rax, -%d(%%rbp)\n", offset);
            }
            break;
        }

        case STMT_SET: {
            // Generate expression (result in %rax)
            codegen_generate_expression(codegen, stmt->data.set_stmt.expression);

            // Find the variable
            int var_index = codegen_find_variable(codegen, stmt->data.set_stmt.variable_name);
            if (var_index == -1) {
                fprintf(stderr, "[CODEGEN ERROR] Unknown variable '%s'\n", stmt->data.set_stmt.variable_name);
                exit(1);
            }
            int offset = codegen->variables[var_index].stack_offset;

            // If we're setting a field, we need to handle it differently
            if (stmt->data.set_stmt.field_name != NULL) {
                // Save expression value
                fprintf(codegen->output_file, "    pushq %%rax\n");

                // Load struct address into %rbx
                fprintf(codegen->output_file, "    leaq -%d(%%rbp), %%rbx\n", offset);

                // Find field offset
                char *type_name = codegen->variables[var_index].type_name;
                if (!type_name) {
                    fprintf(stderr, "[CODEGEN ERROR] Variable '%s' has no type\n", stmt->data.set_stmt.variable_name);
                    exit(1);
                }

                TypeDefinition *type = NULL;
                for (int i = 0; i < codegen->current_program->type_count; i++) {
                    if (strcmp(codegen->current_program->types[i]->name, type_name) == 0) {
                        type = codegen->current_program->types[i];
                        break;
                    }
                }

                if (!type) {
                    fprintf(stderr, "[CODEGEN ERROR] Unknown type '%s' (line %d)\n", type_name, __LINE__);
                    exit(1);
                }

                int field_offset = -1;
                for (int i = 0; i < type->field_count; i++) {
                    if (strcmp(type->fields[i].name, stmt->data.set_stmt.field_name) == 0) {
                        field_offset = type->fields[i].offset;
                        break;
                    }
                }

                if (field_offset == -1) {
                    fprintf(stderr, "[CODEGEN ERROR] Type '%s' has no field '%s'\n", type_name, stmt->data.set_stmt.field_name);
                    exit(1);
                }

                // Restore value and store in field
                fprintf(codegen->output_file, "    popq %%rax\n");
                fprintf(codegen->output_file, "    movq %%rax, %d(%%rbx)\n", field_offset);
            } else {
                // Simple variable assignment
                fprintf(codegen->output_file, "    movq %%rax, -%d(%%rbp)\n", offset);
            }
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
            // Generate expression (result in %rax)
            codegen_generate_expression(codegen, stmt->data.print_stmt.expression);

            // Call appropriate print function based on expression type
            Expression *expr = stmt->data.print_stmt.expression;
            if (expr->type == EXPR_STRING_LITERAL) {
                // String literal - call print_string
                fprintf(codegen->output_file, "    movq %%rax, %%rdi\n");
                fprintf(codegen->output_file, "    call print_string\n");
            } else {
                // Integer expression (variable, literal, arithmetic) - call print_integer
                fprintf(codegen->output_file, "    movq %%rax, %%rdi\n");
                fprintf(codegen->output_file, "    call print_integer\n");
            }
            break;
        }

        case STMT_EXPRESSION:
            // Generate the expression and ignore its result
            codegen_generate_expression(codegen, stmt->data.expr_stmt.expression);
            break;
    }
}

CodeGenerator* codegen_create(const char *output_filename) {
    CodeGenerator *codegen = malloc(sizeof(CodeGenerator));
    codegen->output_file = fopen(output_filename, "w");
    codegen->variable_count = 0;
    codegen->variable_capacity = 16;  // Start with space for 16 variables
    codegen->variables = malloc(sizeof(Variable) * codegen->variable_capacity);
    codegen->stack_offset = 0;
    codegen->label_counter = 0;
    codegen->string_count = 0;
    codegen->string_capacity = 32;   // Start with space for 32 strings
    codegen->strings = malloc(sizeof(StringLiteral) * codegen->string_capacity);
    codegen->current_program = NULL;

    if (!codegen->output_file) {
        fprintf(stderr, "[CODEGEN ERROR] Could not open output file '%s'\n", output_filename);
        free(codegen->variables);
        free(codegen->strings);
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
            free(codegen->variables[i].type_name);
        }
        for (int i = 0; i < codegen->string_count; i++) {
            free(codegen->strings[i].value);
            free(codegen->strings[i].label);
        }
        free(codegen->variables);
        free(codegen->strings);
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

    // Handle parameters (System V ABI: %rdi, %rsi, %rdx, %rcx, %r8, %r9)
    const char *param_registers[] = {"%rdi", "%rsi", "%rdx", "%rcx", "%r8", "%r9"};
    int max_register_params = sizeof(param_registers) / sizeof(param_registers[0]);

    for (int i = 0; i < func->parameter_count && i < max_register_params; i++) {
        // Add parameter as a variable and store from appropriate register
        int param_index = codegen_add_variable(codegen, func->parameters[i].name);
        int param_offset = codegen->variables[param_index].stack_offset;
        fprintf(codegen->output_file, "    movq %s, -%d(%%rbp)\n", param_registers[i], param_offset);
    }

    // Handle parameters beyond 6 (from stack) - not implemented yet
    if (func->parameter_count > max_register_params) {
        fprintf(stderr, "[CODEGEN WARNING] Functions with more than 6 parameters not fully supported yet\n");
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
    // Store program reference for type lookups
    codegen->current_program = program;

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

    // Add print_integer runtime function
    fprintf(codegen->output_file, "print_integer:\n");
    fprintf(codegen->output_file, "    pushq %%rbp\n");
    fprintf(codegen->output_file, "    movq %%rsp, %%rbp\n");
    fprintf(codegen->output_file, "    subq $32, %%rsp  # Space for string buffer (20 digits + null)\n");
    fprintf(codegen->output_file, "    \n");
    fprintf(codegen->output_file, "    # Convert integer to string\n");
    fprintf(codegen->output_file, "    movq %%rdi, %%rax  # integer value\n");
    fprintf(codegen->output_file, "    leaq -32(%%rbp), %%rsi  # buffer pointer\n");
    fprintf(codegen->output_file, "    addq $19, %%rsi  # point to end of buffer (for reverse building)\n");
    fprintf(codegen->output_file, "    movb $0, (%%rsi)  # null terminator\n");
    fprintf(codegen->output_file, "    decq %%rsi\n");
    fprintf(codegen->output_file, "    \n");
    fprintf(codegen->output_file, "    # Handle zero case\n");
    fprintf(codegen->output_file, "    testq %%rax, %%rax\n");
    fprintf(codegen->output_file, "    jnz .convert_loop\n");
    fprintf(codegen->output_file, "    movb $48, (%%rsi)  # '0' character\n");
    fprintf(codegen->output_file, "    jmp .convert_done\n");
    fprintf(codegen->output_file, "    \n");
    fprintf(codegen->output_file, ".convert_loop:\n");
    fprintf(codegen->output_file, "    testq %%rax, %%rax\n");
    fprintf(codegen->output_file, "    jz .convert_done\n");
    fprintf(codegen->output_file, "    movq %%rax, %%rcx\n");
    fprintf(codegen->output_file, "    movq $10, %%rbx\n");
    fprintf(codegen->output_file, "    xorq %%rdx, %%rdx\n");
    fprintf(codegen->output_file, "    divq %%rbx  # %%rax = quotient, %%rdx = remainder\n");
    fprintf(codegen->output_file, "    addq $48, %%rdx  # convert remainder to ASCII\n");
    fprintf(codegen->output_file, "    movb %%dl, (%%rsi)  # store digit\n");
    fprintf(codegen->output_file, "    decq %%rsi\n");
    fprintf(codegen->output_file, "    jmp .convert_loop\n");
    fprintf(codegen->output_file, "    \n");
    fprintf(codegen->output_file, ".convert_done:\n");
    fprintf(codegen->output_file, "    incq %%rsi  # point to first character\n");
    fprintf(codegen->output_file, "    \n");
    fprintf(codegen->output_file, "    # Calculate string length\n");
    fprintf(codegen->output_file, "    movq %%rsi, %%rcx  # Counter for strlen\n");
    fprintf(codegen->output_file, "    xorq %%rax, %%rax  # Length accumulator\n");
    fprintf(codegen->output_file, ".int_strlen_loop:\n");
    fprintf(codegen->output_file, "    cmpb $0, (%%rcx)\n");
    fprintf(codegen->output_file, "    je .int_strlen_done\n");
    fprintf(codegen->output_file, "    incq %%rcx\n");
    fprintf(codegen->output_file, "    incq %%rax\n");
    fprintf(codegen->output_file, "    jmp .int_strlen_loop\n");
    fprintf(codegen->output_file, ".int_strlen_done:\n");
    fprintf(codegen->output_file, "    \n");
    fprintf(codegen->output_file, "    # Call write syscall (sys_write = 1)\n");
    fprintf(codegen->output_file, "    movq $1, %%rdi     # fd = stdout\n");
    fprintf(codegen->output_file, "    # %%rsi already points to string\n");
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
    fprintf(codegen->output_file, "    movq %%rbp, %%rsp\n");
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

    // Add GNU stack note to prevent executable stack warning
    fprintf(codegen->output_file, "\n.section .note.GNU-stack,\"\",@progbits\n");
}