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

        case EXPR_BUILTIN_CALL:
            for (int i = 0; i < expr->data.builtin_call.argument_count; i++) {
                codegen_collect_strings_from_expression(codegen, expr->data.builtin_call.arguments[i]);
            }
            break;
        case EXPR_VARIANT_CONSTRUCTOR:
            for (int i = 0; i < expr->data.variant_constructor.field_count; i++) {
                codegen_collect_strings_from_expression(codegen, expr->data.variant_constructor.field_values[i]);
            }
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
            codegen_collect_strings_from_expression(codegen, stmt->data.set_stmt.target);
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

        case STMT_IMPORT:
            // Imports don't have strings to collect
            break;
        case STMT_MATCH:
            codegen_collect_strings_from_expression(codegen, stmt->data.match_stmt.expression);
            for (int i = 0; i < stmt->data.match_stmt.case_count; i++) {
                MatchCase *match_case = &stmt->data.match_stmt.cases[i];
                for (int j = 0; j < match_case->body_count; j++) {
                    codegen_collect_strings_from_statement(codegen, match_case->body[j]);
                }
            }
            break;
    }
}

// Helper function to determine the type name of an expression
static char* codegen_get_expression_type(CodeGenerator *codegen, Expression *expr) {
    switch (expr->type) {
        case EXPR_VARIABLE: {
            int var_index = codegen_find_variable(codegen, expr->data.variable_name);
            if (var_index == -1) {
                return NULL;
            }
            return codegen->variables[var_index].type_name;
        }

        case EXPR_FIELD_ACCESS: {
            // Get the type of the object
            char *object_type = codegen_get_expression_type(codegen, expr->data.field_access.object);
            if (!object_type) {
                return NULL;
            }

            // Find the type definition
            TypeDefinition *type = NULL;
            for (int i = 0; i < codegen->current_program->type_count; i++) {
                if (strcmp(codegen->current_program->types[i]->name, object_type) == 0) {
                    type = codegen->current_program->types[i];
                    break;
                }
            }

            if (!type) {
                return NULL;
            }

            // Find the field and return its type
            char *field_name = expr->data.field_access.field_name;
            if (type->kind == TYPE_KIND_STRUCT) {
                for (int i = 0; i < type->data.struct_type.field_count; i++) {
                    if (strcmp(type->data.struct_type.fields[i].name, field_name) == 0) {
                        return type->data.struct_type.fields[i].type;
                    }
                }
            }

            return NULL;
        }

        default:
            return NULL;
    }
}

// Generate the address of an lvalue expression (result in %rbx)
static void codegen_generate_lvalue_address(CodeGenerator *codegen, Expression *expr) {
    switch (expr->type) {
        case EXPR_VARIABLE: {
            // Find variable and generate its address
            int var_index = codegen_find_variable(codegen, expr->data.variable_name);
            if (var_index == -1) {
                fprintf(stderr, "[CODEGEN ERROR] Unknown variable '%s'\n", expr->data.variable_name);
                exit(1);
            }
            int offset = codegen->variables[var_index].stack_offset;

            // Generate address of variable on stack
            fprintf(codegen->output_file, "    leaq -%d(%%rbp), %%rbx\n", offset);
            break;
        }

        case EXPR_FIELD_ACCESS: {
            // Generate address of object
            codegen_generate_lvalue_address(codegen, expr->data.field_access.object);

            // Now %rbx contains the address of the object
            // We need to add the field offset to get the field address

            // Get the type of the object using our helper function
            char *object_type = codegen_get_expression_type(codegen, expr->data.field_access.object);
            if (!object_type) {
                fprintf(stderr, "[CODEGEN ERROR] Cannot determine type of object in field access\n");
                exit(1);
            }

            // Find the type definition
            TypeDefinition *type = NULL;
            for (int i = 0; i < codegen->current_program->type_count; i++) {
                if (strcmp(codegen->current_program->types[i]->name, object_type) == 0) {
                    type = codegen->current_program->types[i];
                    break;
                }
            }

            if (!type) {
                fprintf(stderr, "[CODEGEN ERROR] Unknown type '%s'\n", object_type);
                exit(1);
            }

            // Find field offset
            char *field_name = expr->data.field_access.field_name;
            int field_offset = -1;
            if (type->kind == TYPE_KIND_STRUCT) {
                for (int i = 0; i < type->data.struct_type.field_count; i++) {
                    if (strcmp(type->data.struct_type.fields[i].name, field_name) == 0) {
                        field_offset = type->data.struct_type.fields[i].offset;
                        break;
                    }
                }
            }

            if (field_offset == -1) {
                fprintf(stderr, "[CODEGEN ERROR] Type '%s' has no field '%s'\n", object_type, field_name);
                exit(1);
            }

            // Add field offset to object address
            fprintf(codegen->output_file, "    addq $%d, %%rbx\n", field_offset);
            break;
        }

        default:
            fprintf(stderr, "[CODEGEN ERROR] Invalid lvalue expression type\n");
            exit(1);
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
            } else if (expr->data.comparison.comparison_op == TOKEN_NOT_EQUAL) {
                fprintf(codegen->output_file, "    setne %%al\n");
            } else if (expr->data.comparison.comparison_op == TOKEN_LESS) {
                fprintf(codegen->output_file, "    setl %%al\n");
            } else if (expr->data.comparison.comparison_op == TOKEN_GREATER) {
                fprintf(codegen->output_file, "    setg %%al\n");
            } else if (expr->data.comparison.comparison_op == TOKEN_LESS_EQUAL) {
                fprintf(codegen->output_file, "    setle %%al\n");
            } else if (expr->data.comparison.comparison_op == TOKEN_GREATER_EQUAL) {
                fprintf(codegen->output_file, "    setge %%al\n");
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

        case EXPR_BUILTIN_CALL: {
            // Handle built-in functions
            const char *func_name;
            if (expr->data.builtin_call.builtin_type == TOKEN_READ_FILE) {
                func_name = "runtime_read_file";
            } else if (expr->data.builtin_call.builtin_type == TOKEN_WRITE_FILE) {
                func_name = "runtime_write_file";
            } else if (expr->data.builtin_call.builtin_type == TOKEN_STRING_LENGTH) {
                func_name = "string_length";
            } else if (expr->data.builtin_call.builtin_type == TOKEN_STRING_CHAR_AT) {
                func_name = "string_char_at";
            } else if (expr->data.builtin_call.builtin_type == TOKEN_STRING_SUBSTRING) {
                func_name = "string_substring";
            } else if (expr->data.builtin_call.builtin_type == TOKEN_STRING_EQUALS) {
                func_name = "string_equals";
            } else if (expr->data.builtin_call.builtin_type == TOKEN_ASCII_VALUE_OF) {
                func_name = "ascii_value_of";
            } else if (expr->data.builtin_call.builtin_type == TOKEN_IS_DIGIT) {
                func_name = "is_digit";
            } else if (expr->data.builtin_call.builtin_type == TOKEN_IS_ALPHA) {
                func_name = "is_alpha";
            } else if (expr->data.builtin_call.builtin_type == TOKEN_IS_WHITESPACE) {
                func_name = "is_whitespace";
            } else if (expr->data.builtin_call.builtin_type == TOKEN_LIST_CREATE) {
                func_name = "list_create";
            } else if (expr->data.builtin_call.builtin_type == TOKEN_LIST_APPEND) {
                func_name = "list_append";
            } else if (expr->data.builtin_call.builtin_type == TOKEN_LIST_GET) {
                func_name = "list_get";
            } else if (expr->data.builtin_call.builtin_type == TOKEN_LIST_GET_INTEGER) {
                func_name = "list_get_integer";
            } else if (expr->data.builtin_call.builtin_type == TOKEN_LIST_LENGTH) {
                func_name = "list_length";
            } else if (expr->data.builtin_call.builtin_type == TOKEN_LIST_DESTROY) {
                func_name = "list_destroy";
            } else {
                fprintf(stderr, "[CODEGEN ERROR] Unknown built-in function type\n");
                exit(1);
            }

            // System V ABI: arguments go in %rdi, %rsi
            const char *arg_registers[] = {"%rdi", "%rsi", "%rdx", "%rcx", "%r8", "%r9"};
            int arg_count = expr->data.builtin_call.argument_count;

            // Validate argument count
            if (expr->data.builtin_call.builtin_type == TOKEN_READ_FILE) {
                if (arg_count != 1) {
                    fprintf(stderr, "[CODEGEN ERROR] read_file expects 1 argument, got %d\n", arg_count);
                    exit(1);
                }
            } else if (expr->data.builtin_call.builtin_type == TOKEN_WRITE_FILE) {
                if (arg_count != 2) {
                    fprintf(stderr, "[CODEGEN ERROR] write_file expects 2 arguments, got %d\n", arg_count);
                    exit(1);
                }
            } else if (expr->data.builtin_call.builtin_type == TOKEN_STRING_LENGTH ||
                      expr->data.builtin_call.builtin_type == TOKEN_ASCII_VALUE_OF ||
                      expr->data.builtin_call.builtin_type == TOKEN_IS_DIGIT ||
                      expr->data.builtin_call.builtin_type == TOKEN_IS_ALPHA ||
                      expr->data.builtin_call.builtin_type == TOKEN_IS_WHITESPACE) {
                if (arg_count != 1) {
                    fprintf(stderr, "[CODEGEN ERROR] %s expects 1 argument, got %d\n", func_name, arg_count);
                    exit(1);
                }
            } else if (expr->data.builtin_call.builtin_type == TOKEN_STRING_CHAR_AT ||
                      expr->data.builtin_call.builtin_type == TOKEN_STRING_EQUALS) {
                if (arg_count != 2) {
                    fprintf(stderr, "[CODEGEN ERROR] %s expects 2 arguments, got %d\n", func_name, arg_count);
                    exit(1);
                }
            } else if (expr->data.builtin_call.builtin_type == TOKEN_STRING_SUBSTRING) {
                if (arg_count != 3) {
                    fprintf(stderr, "[CODEGEN ERROR] string_substring expects 3 arguments, got %d\n", arg_count);
                    exit(1);
                }
            } else if (expr->data.builtin_call.builtin_type == TOKEN_LIST_CREATE) {
                if (arg_count != 0) {
                    fprintf(stderr, "[CODEGEN ERROR] list_create expects 0 arguments, got %d\n", arg_count);
                    exit(1);
                }
            } else if (expr->data.builtin_call.builtin_type == TOKEN_LIST_LENGTH ||
                      expr->data.builtin_call.builtin_type == TOKEN_LIST_DESTROY) {
                if (arg_count != 1) {
                    fprintf(stderr, "[CODEGEN ERROR] %s expects 1 argument, got %d\n", func_name, arg_count);
                    exit(1);
                }
            } else if (expr->data.builtin_call.builtin_type == TOKEN_LIST_GET ||
                      expr->data.builtin_call.builtin_type == TOKEN_LIST_GET_INTEGER ||
                      expr->data.builtin_call.builtin_type == TOKEN_LIST_APPEND) {
                if (arg_count != 2) {
                    fprintf(stderr, "[CODEGEN ERROR] %s expects 2 arguments, got %d\n", func_name, arg_count);
                    exit(1);
                }
            }

            // Evaluate arguments in reverse order and push them to stack
            for (int i = arg_count - 1; i >= 0; i--) {
                codegen_generate_expression(codegen, expr->data.builtin_call.arguments[i]);
                fprintf(codegen->output_file, "    pushq %%rax\n");
            }

            // Pop arguments into correct registers
            for (int i = 0; i < arg_count; i++) {
                fprintf(codegen->output_file, "    popq %s\n", arg_registers[i]);
            }

            // Call the runtime function
            fprintf(codegen->output_file, "    call %s@PLT\n", func_name);
            // Result is in %rax
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

                // Find the field offset based on the variable's type
                char *type_name = codegen->variables[var_index].type_name;
                int offset = codegen->variables[var_index].stack_offset;

                if (!type_name || strcmp(type_name, "Integer") == 0) {
                    // Variable is untyped/Integer - treat as raw pointer
                    // Load the pointer value
                    fprintf(codegen->output_file, "    movq -%d(%%rbp), %%rax\n", offset);

                    // For raw pointer access, we need to determine field offset
                    // For now, we'll use a simple heuristic based on field name
                    int field_offset = 0;

                    // Common field patterns from our transliterated code
                    if (strcmp(expr->data.field_access.field_name, "type") == 0) {
                        field_offset = 0;
                    } else if (strcmp(expr->data.field_access.field_name, "value") == 0) {
                        field_offset = 8;
                    } else if (strcmp(expr->data.field_access.field_name, "line") == 0) {
                        field_offset = 16;
                    } else if (strcmp(expr->data.field_access.field_name, "column") == 0) {
                        field_offset = 24;
                    } else if (strcmp(expr->data.field_access.field_name, "source") == 0) {
                        field_offset = 0;
                    } else if (strcmp(expr->data.field_access.field_name, "position") == 0) {
                        field_offset = 8;
                    } else if (strcmp(expr->data.field_access.field_name, "current_char") == 0) {
                        field_offset = 32;
                    } else {
                        // Default to sequential 8-byte offsets
                        // This is a simplification - real implementation would track types
                        field_offset = 0;
                    }

                    // Load the field value
                    fprintf(codegen->output_file, "    movq %d(%%rax), %%rax\n", field_offset);
                } else {
                    // Variable has a type - use type information
                    // Load the address of the struct
                    fprintf(codegen->output_file, "    leaq -%d(%%rbp), %%rax\n", offset);

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
                    if (type->kind == TYPE_KIND_STRUCT) {
                        for (int i = 0; i < type->data.struct_type.field_count; i++) {
                            if (strcmp(type->data.struct_type.fields[i].name, expr->data.field_access.field_name) == 0) {
                                field_offset = type->data.struct_type.fields[i].offset;
                                break;
                            }
                        }
                    }

                    if (field_offset == -1) {
                        fprintf(stderr, "[CODEGEN ERROR] Type '%s' has no field '%s'\n", type_name, expr->data.field_access.field_name);
                        exit(1);
                    }

                    // Load the field value
                    fprintf(codegen->output_file, "    movq %d(%%rax), %%rax\n", field_offset);
                }
            } else {
                // Handle complex field access expressions (nested access)
                // For nested access, we need the ADDRESS of the intermediate object,
                // not its value. Use the lvalue addressing logic.
                codegen_generate_lvalue_address(codegen, obj);

                // Now %rbx contains the address of the object, copy to %rax
                fprintf(codegen->output_file, "    movq %%rbx, %%rax\n");
                // Get the type of the object expression
                char *object_type = codegen_get_expression_type(codegen, obj);
                if (!object_type) {
                    fprintf(stderr, "[CODEGEN ERROR] Cannot determine type of complex field access object\n");
                    exit(1);
                }

                // Find the type definition for the object type
                TypeDefinition *type = NULL;
                for (int i = 0; i < codegen->current_program->type_count; i++) {
                    if (strcmp(codegen->current_program->types[i]->name, object_type) == 0) {
                        type = codegen->current_program->types[i];
                        break;
                    }
                }

                if (!type) {
                    fprintf(stderr, "[CODEGEN ERROR] Unknown type '%s' in complex field access\n", object_type);
                    exit(1);
                }

                // Find the field offset
                int field_offset = -1;
                if (type->kind == TYPE_KIND_STRUCT) {
                    for (int i = 0; i < type->data.struct_type.field_count; i++) {
                        if (strcmp(type->data.struct_type.fields[i].name, expr->data.field_access.field_name) == 0) {
                            field_offset = type->data.struct_type.fields[i].offset;
                            break;
                        }
                    }
                }

                if (field_offset == -1) {
                    fprintf(stderr, "[CODEGEN ERROR] Type '%s' has no field '%s'\n", object_type, expr->data.field_access.field_name);
                    exit(1);
                }

                // Add the field offset to the address in %rax
                if (field_offset > 0) {
                    fprintf(codegen->output_file, "    addq $%d, %%rax\n", field_offset);
                }

                // Load the field value
                fprintf(codegen->output_file, "    movq (%%rax), %%rax\n");
            }
            break;
        }

        case EXPR_TYPE_NAME:
            // Type names don't generate code directly - they're handled in LET statements
            // This shouldn't be reached in normal execution
            fprintf(stderr, "[CODEGEN ERROR] Type names should only appear in LET statements\n");
            exit(1);
            break;

        case EXPR_VARIANT_CONSTRUCTOR: {
            // Find the type definition
            TypeDefinition *type = NULL;
            for (int i = 0; i < codegen->current_program->type_count; i++) {
                if (strcmp(codegen->current_program->types[i]->name, expr->data.variant_constructor.type_name) == 0) {
                    type = codegen->current_program->types[i];
                    break;
                }
            }

            if (!type || type->kind != TYPE_KIND_VARIANT) {
                fprintf(stderr, "[CODEGEN ERROR] Unknown variant type '%s'\n",
                        expr->data.variant_constructor.type_name);
                exit(1);
            }

            // Find the variant
            Variant *variant = NULL;
            for (int i = 0; i < type->data.variant_type.variant_count; i++) {
                if (strcmp(type->data.variant_type.variants[i].name,
                          expr->data.variant_constructor.variant_name) == 0) {
                    variant = &type->data.variant_type.variants[i];
                    break;
                }
            }

            if (!variant) {
                fprintf(stderr, "[CODEGEN ERROR] Unknown variant '%s' in type '%s'\n",
                        expr->data.variant_constructor.variant_name,
                        expr->data.variant_constructor.type_name);
                exit(1);
            }

            // Allocate memory for the variant
            fprintf(codegen->output_file, "    # Construct variant %s::%s\n",
                    type->name, variant->name);
            fprintf(codegen->output_file, "    movq $%d, %%rdi\n", type->size);
            fprintf(codegen->output_file, "    call malloc\n");
            fprintf(codegen->output_file, "    pushq %%rax  # Save variant pointer\n");

            // Store the tag (variant index)
            fprintf(codegen->output_file, "    movq $%d, (%%rax)  # Store variant tag\n", variant->tag);

            // Store field values
            for (int i = 0; i < expr->data.variant_constructor.field_count; i++) {
                // Evaluate field value
                codegen_generate_expression(codegen, expr->data.variant_constructor.field_values[i]);

                // Store in the variant at the right offset
                fprintf(codegen->output_file, "    popq %%rdi  # Restore variant pointer\n");
                fprintf(codegen->output_file, "    pushq %%rdi  # Keep it on stack\n");
                fprintf(codegen->output_file, "    movq %%rax, %d(%%rdi)  # Store field at offset %d\n",
                        variant->fields[i].offset, variant->fields[i].offset);
            }

            // Leave the variant pointer in %rax
            fprintf(codegen->output_file, "    popq %%rax  # Final variant pointer\n");
            break;
        }
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
                // Check if the expression returns a string or list
                Expression *expr = stmt->data.let_stmt.expression;
                if (expr->type == EXPR_BUILTIN_CALL &&
                    (expr->data.builtin_call.builtin_type == TOKEN_READ_FILE ||
                     expr->data.builtin_call.builtin_type == TOKEN_STRING_SUBSTRING)) {
                    // This is a string-returning expression
                    codegen_add_variable_with_type(codegen, stmt->data.let_stmt.variable_name, "String");
                } else if (expr->type == EXPR_BUILTIN_CALL &&
                          expr->data.builtin_call.builtin_type == TOKEN_LIST_CREATE) {
                    // This is a list-returning expression
                    codegen_add_variable_with_type(codegen, stmt->data.let_stmt.variable_name, "List");
                } else {
                    // Regular integer/other expression
                    codegen_add_variable(codegen, stmt->data.let_stmt.variable_name);
                }

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
            // Generate value expression (result in %rax)
            codegen_generate_expression(codegen, stmt->data.set_stmt.expression);

            // Save the value on the stack
            fprintf(codegen->output_file, "    pushq %%rax\n");

            // Generate the address of the target (result in %rbx)
            codegen_generate_lvalue_address(codegen, stmt->data.set_stmt.target);

            // Restore value and store to target address
            fprintf(codegen->output_file, "    popq %%rax\n");
            fprintf(codegen->output_file, "    movq %%rax, (%%rbx)\n");
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
            } else if (expr->type == EXPR_BUILTIN_CALL &&
                      (expr->data.builtin_call.builtin_type == TOKEN_READ_FILE ||
                       expr->data.builtin_call.builtin_type == TOKEN_STRING_SUBSTRING)) {
                // read_file and string_substring return strings - call print_string
                fprintf(codegen->output_file, "    movq %%rax, %%rdi\n");
                fprintf(codegen->output_file, "    call print_string\n");
            } else if (expr->type == EXPR_VARIABLE) {
                // Check variable type to determine appropriate print function
                int var_index = codegen_find_variable(codegen, expr->data.variable_name);
                if (var_index != -1 && codegen->variables[var_index].type_name &&
                    strcmp(codegen->variables[var_index].type_name, "String") == 0) {
                    // This variable contains a string - call print_string
                    fprintf(codegen->output_file, "    movq %%rax, %%rdi\n");
                    fprintf(codegen->output_file, "    call print_string\n");
                } else if (var_index != -1 && codegen->variables[var_index].type_name &&
                          strcmp(codegen->variables[var_index].type_name, "List") == 0) {
                    // This variable contains a list pointer - print as integer address for now
                    fprintf(codegen->output_file, "    movq %%rax, %%rdi\n");
                    fprintf(codegen->output_file, "    call print_integer\n");
                } else {
                    // Assume integer for other variables
                    fprintf(codegen->output_file, "    movq %%rax, %%rdi\n");
                    fprintf(codegen->output_file, "    call print_integer\n");
                }
            } else {
                // Integer expression (literal, arithmetic) - call print_integer
                fprintf(codegen->output_file, "    movq %%rax, %%rdi\n");
                fprintf(codegen->output_file, "    call print_integer\n");
            }
            break;
        }

        case STMT_EXPRESSION:
            // Generate the expression and ignore its result
            codegen_generate_expression(codegen, stmt->data.expr_stmt.expression);
            break;

        case STMT_IMPORT:
            // Imports are handled at program level, no code generation needed
            break;

        case STMT_MATCH: {
            // Evaluate the expression to match on
            codegen_generate_expression(codegen, stmt->data.match_stmt.expression);
            fprintf(codegen->output_file, "    pushq %%rax  # Save match expression value\n");

            // Generate unique labels for each case and the end
            int match_id = codegen->label_counter++;
            char end_label[256];
            snprintf(end_label, sizeof(end_label), ".match_end_%d", match_id);

            // Generate code for each case
            for (int i = 0; i < stmt->data.match_stmt.case_count; i++) {
                MatchCase *match_case = &stmt->data.match_stmt.cases[i];
                char case_label[256];
                char next_label[256];
                snprintf(case_label, sizeof(case_label), ".match_case_%d_%d", match_id, i);
                snprintf(next_label, sizeof(next_label), ".match_case_%d_%d",
                        match_id, i + 1);

                // Check if this case matches
                fprintf(codegen->output_file, "%s:\n", case_label);
                fprintf(codegen->output_file, "    popq %%rax  # Get match expression\n");
                fprintf(codegen->output_file, "    pushq %%rax  # Keep on stack\n");

                // Load the tag from the variant
                fprintf(codegen->output_file, "    movq (%%rax), %%rdx  # Load variant tag\n");

                // Find the tag value for this variant name
                // We need to find the type and variant to get the tag
                // For now, assume tags are sequential starting from 0
                fprintf(codegen->output_file, "    cmpq $%d, %%rdx  # Check tag for %s\n",
                        i, match_case->variant_name);

                if (i < stmt->data.match_stmt.case_count - 1) {
                    fprintf(codegen->output_file, "    jne %s  # Jump to next case\n", next_label);
                } else {
                    fprintf(codegen->output_file, "    jne %s  # No match, exit\n", end_label);
                }

                // If we matched, extract fields and bind to local variables
                if (match_case->field_count > 0) {
                    // Pop the variant pointer
                    fprintf(codegen->output_file, "    popq %%rax  # Get variant pointer\n");
                    fprintf(codegen->output_file, "    pushq %%rax  # Keep on stack\n");

                    // We'd need to find the variant definition to know field offsets
                    // For now, assume fields start at offset 8 (after tag) and are 8 bytes each
                    for (int j = 0; j < match_case->field_count; j++) {
                        int field_offset = 8 + j * 8;
                        fprintf(codegen->output_file, "    movq %d(%%rax), %%rdx  # Load field %d\n",
                                field_offset, j);

                        // Create a local variable for the binding - allocate stack space properly
                        codegen->stack_offset += 8;
                        fprintf(codegen->output_file, "    movq %%rdx, -%d(%%rbp)  # Store %s at stack offset\n",
                                codegen->stack_offset, match_case->field_names[j]);

                        // Add the binding to the variable table with correct offset
                        int var_idx = codegen->variable_count;
                        if (codegen->variable_count >= codegen->variable_capacity) {
                            codegen->variable_capacity *= 2;
                            codegen->variables = realloc(codegen->variables,
                                                       sizeof(Variable) * codegen->variable_capacity);
                        }
                        codegen->variables[var_idx].name = string_duplicate(match_case->field_names[j]);
                        codegen->variables[var_idx].stack_offset = codegen->stack_offset;
                        codegen->variables[var_idx].type_name = string_duplicate("Integer");
                        codegen->variable_count++;
                    }
                }

                // Generate the case body
                for (int j = 0; j < match_case->body_count; j++) {
                    codegen_generate_statement(codegen, match_case->body[j]);
                }

                // Clean up bindings from variable table but keep stack offset
                // (we need to track max stack usage for proper allocation)
                if (match_case->field_count > 0) {
                    // Free the variable names we allocated
                    for (int j = 0; j < match_case->field_count; j++) {
                        int var_idx = codegen->variable_count - match_case->field_count + j;
                        free(codegen->variables[var_idx].name);
                        free(codegen->variables[var_idx].type_name);
                    }
                    // Don't decrease stack_offset - we need to track maximum usage
                    // Also remove from variable table
                    codegen->variable_count -= match_case->field_count;
                }

                // Jump to end
                fprintf(codegen->output_file, "    jmp %s\n", end_label);
            }

            fprintf(codegen->output_file, "%s:\n", end_label);
            fprintf(codegen->output_file, "    popq %%rax  # Clean up match expression\n");
            break;
        }
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

    // Export function as global symbol for cross-module linking
    fprintf(codegen->output_file, ".globl %s\n", func->name);

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

    // Generate import comments (for documentation)
    if (program->import_count > 0) {
        fprintf(codegen->output_file, "# Imports:\n");
        for (int i = 0; i < program->import_count; i++) {
            fprintf(codegen->output_file, "#   Import \"%s\" as %s\n",
                    program->imports[i]->filename,
                    program->imports[i]->module_name);
        }
        fprintf(codegen->output_file, "\n");
    }

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