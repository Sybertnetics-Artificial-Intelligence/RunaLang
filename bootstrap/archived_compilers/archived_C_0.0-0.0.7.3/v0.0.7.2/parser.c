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
#include "parser.h"

// Forward declarations
static Statement* parser_parse_if_statement(Parser *parser);
static Statement* parser_parse_while_statement(Parser *parser);
static Statement* parser_parse_print_statement(Parser *parser);
static Statement* parser_parse_match_statement(Parser *parser);
static Statement* parser_parse_inline_assembly_statement(Parser *parser);
static Expression* parser_parse_expression(Parser *parser);

static char* string_duplicate(const char *str) {
    if (!str) return NULL;
    int len = strlen(str);
    char *dup = malloc(len + 1);
    strcpy(dup, str);
    return dup;
}

static void parser_advance(Parser *parser) {
    token_destroy(parser->current_token);
    parser->current_token = lexer_next_token(parser->lexer);
}

static void parser_eat(Parser *parser, TokenType expected_type) {
    if (parser->current_token->type == expected_type) {
        parser_advance(parser);
    } else {
        fprintf(stderr, "[PARSER ERROR] Expected token type %d, got %d at line %d\n",
                expected_type, parser->current_token->type, parser->current_token->line);
        exit(1);
    }
}

static int parser_is_builtin_function_token(TokenType type) {
    return (type == TOKEN_READ_FILE ||
            type == TOKEN_WRITE_FILE ||
            type == TOKEN_STRING_LENGTH ||
            type == TOKEN_STRING_CHAR_AT ||
            type == TOKEN_STRING_SUBSTRING ||
            type == TOKEN_STRING_EQUALS ||
            type == TOKEN_ASCII_VALUE_OF ||
            type == TOKEN_IS_DIGIT ||
            type == TOKEN_IS_ALPHA ||
            type == TOKEN_IS_WHITESPACE ||
            type == TOKEN_STRING_CONCAT ||
            type == TOKEN_STRING_COMPARE ||
            type == TOKEN_STRING_TO_INTEGER ||
            type == TOKEN_INTEGER_TO_STRING ||
            type == TOKEN_STRING_FIND ||
            type == TOKEN_STRING_REPLACE ||
            type == TOKEN_STRING_TRIM ||
            type == TOKEN_STRING_SPLIT ||
            type == TOKEN_LIST_CREATE ||
            type == TOKEN_LIST_APPEND ||
            type == TOKEN_LIST_GET ||
            type == TOKEN_LIST_GET_INTEGER ||
            type == TOKEN_LIST_LENGTH ||
            type == TOKEN_LIST_DESTROY ||
            type == TOKEN_LIST_SET ||
            type == TOKEN_LIST_INSERT ||
            type == TOKEN_LIST_REMOVE ||
            type == TOKEN_LIST_CLEAR ||
            type == TOKEN_LIST_FIND ||
            type == TOKEN_LIST_SORT ||
            type == TOKEN_LIST_REVERSE ||
            type == TOKEN_LIST_COPY ||
            type == TOKEN_LIST_MERGE ||
            type == TOKEN_FILE_OPEN ||
            type == TOKEN_FILE_CLOSE ||
            type == TOKEN_FILE_READ_LINE ||
            type == TOKEN_FILE_WRITE_LINE ||
            type == TOKEN_FILE_EXISTS ||
            type == TOKEN_FILE_DELETE ||
            type == TOKEN_FILE_SIZE ||
            type == TOKEN_FILE_SEEK ||
            type == TOKEN_FILE_TELL ||
            type == TOKEN_FILE_EOF ||
            type == TOKEN_SIN ||
            type == TOKEN_COS ||
            type == TOKEN_TAN ||
            type == TOKEN_SQRT ||
            type == TOKEN_POW ||
            type == TOKEN_ABS ||
            type == TOKEN_FLOOR ||
            type == TOKEN_CEIL ||
            type == TOKEN_MIN ||
            type == TOKEN_MAX ||
            type == TOKEN_RANDOM ||
            type == TOKEN_LOG ||
            type == TOKEN_EXP ||
            type == TOKEN_GET_COMMAND_LINE_ARGS ||
            type == TOKEN_EXIT_WITH_CODE ||
            type == TOKEN_PANIC ||
            type == TOKEN_ASSERT ||
            type == TOKEN_ALLOCATE ||
            type == TOKEN_DEALLOCATE);
}

// Forward declarations
static Expression* parser_parse_comparison(Parser *parser);

static Expression* expression_create_integer(int value) {
    Expression *expr = malloc(sizeof(Expression));
    expr->type = EXPR_INTEGER;
    expr->data.integer_value = value;
    return expr;
}

static Expression* expression_create_variable(const char *name) {
    Expression *expr = malloc(sizeof(Expression));
    expr->type = EXPR_VARIABLE;
    expr->data.variable_name = string_duplicate(name);
    return expr;
}

static Expression* expression_create_binary_op(Expression *left, TokenType operator, Expression *right) {
    Expression *expr = malloc(sizeof(Expression));
    expr->type = EXPR_BINARY_OP;
    expr->data.binary_op.left = left;
    expr->data.binary_op.right = right;
    expr->data.binary_op.operator = operator;
    return expr;
}

static Expression* expression_create_comparison(Expression *left, TokenType comparison_op, Expression *right) {
    Expression *expr = malloc(sizeof(Expression));
    expr->type = EXPR_COMPARISON;
    expr->data.comparison.left = left;
    expr->data.comparison.right = right;
    expr->data.comparison.comparison_op = comparison_op;
    return expr;
}

static Expression* expression_create_function_call(const char *function_name, Expression **arguments, int argument_count) {
    Expression *expr = malloc(sizeof(Expression));
    expr->type = EXPR_FUNCTION_CALL;
    expr->data.function_call.function_name = string_duplicate(function_name);
    expr->data.function_call.arguments = arguments;
    expr->data.function_call.argument_count = argument_count;
    return expr;
}

static Expression* expression_create_string_literal_owned(char *string_value) {
    Expression *expr = malloc(sizeof(Expression));
    expr->type = EXPR_STRING_LITERAL;
    expr->data.string_literal = string_value; // Takes ownership
    return expr;
}

static Statement* statement_create_let(const char *var_name, Expression *expr) {
    Statement *stmt = malloc(sizeof(Statement));
    stmt->type = STMT_LET;
    stmt->data.let_stmt.variable_name = string_duplicate(var_name);
    stmt->data.let_stmt.expression = expr;
    return stmt;
}

static Statement* statement_create_set(Expression *target, Expression *expr) {
    Statement *stmt = malloc(sizeof(Statement));
    stmt->type = STMT_SET;
    stmt->data.set_stmt.target = target;
    stmt->data.set_stmt.expression = expr;
    return stmt;
}

static Statement* statement_create_return(Expression *expr) {
    Statement *stmt = malloc(sizeof(Statement));
    stmt->type = STMT_RETURN;
    stmt->data.return_stmt.expression = expr;
    return stmt;
}

static Statement* statement_create_print(Expression *expr) {
    Statement *stmt = malloc(sizeof(Statement));
    stmt->type = STMT_PRINT;
    stmt->data.print_stmt.expression = expr;
    return stmt;
}

static Statement* statement_create_expression(Expression *expr) {
    Statement *stmt = malloc(sizeof(Statement));
    stmt->type = STMT_EXPRESSION;
    stmt->data.expr_stmt.expression = expr;
    return stmt;
}

static Statement* statement_create_if(Expression *condition, Statement **if_body, int if_body_count, Statement **else_body, int else_body_count) {
    Statement *stmt = malloc(sizeof(Statement));
    stmt->type = STMT_IF;
    stmt->data.if_stmt.condition = condition;
    stmt->data.if_stmt.if_body = if_body;
    stmt->data.if_stmt.if_body_count = if_body_count;
    stmt->data.if_stmt.else_body = else_body;
    stmt->data.if_stmt.else_body_count = else_body_count;
    return stmt;
}

static Statement* statement_create_while(Expression *condition, Statement **body, int body_count) {
    Statement *stmt = malloc(sizeof(Statement));
    stmt->type = STMT_WHILE;
    stmt->data.while_stmt.condition = condition;
    stmt->data.while_stmt.body = body;
    stmt->data.while_stmt.body_count = body_count;
    return stmt;
}

static Statement* statement_create_break(void) {
    Statement *stmt = malloc(sizeof(Statement));
    stmt->type = STMT_BREAK;
    return stmt;
}

static Statement* statement_create_continue(void) {
    Statement *stmt = malloc(sizeof(Statement));
    stmt->type = STMT_CONTINUE;
    return stmt;
}

static Function* function_create(const char *name, char *return_type) {
    Function *func = malloc(sizeof(Function));
    func->name = string_duplicate(name);
    func->parameters = NULL;
    func->parameter_count = 0;
    func->return_type = string_duplicate(return_type);
    func->statements = NULL;
    func->statement_count = 0;
    return func;
}

static void function_add_parameter(Function *func, const char *param_name, const char *param_type) {
    func->parameters = realloc(func->parameters, sizeof(Parameter) * (func->parameter_count + 1));
    func->parameters[func->parameter_count].name = string_duplicate(param_name);
    func->parameters[func->parameter_count].type = string_duplicate(param_type);
    func->parameter_count++;
}

static void function_add_statement(Function *func, Statement *stmt) {
    func->statements = realloc(func->statements, sizeof(Statement*) * (func->statement_count + 1));
    func->statements[func->statement_count++] = stmt;
}

static Program* program_create(void) {
    Program *program = malloc(sizeof(Program));
    program->functions = NULL;
    program->function_count = 0;
    program->function_capacity = 0;
    program->types = NULL;
    program->type_count = 0;
    program->type_capacity = 0;
    program->imports = NULL;
    program->import_count = 0;
    program->import_capacity = 0;
    return program;
}

static void program_add_function(Program *program, Function *func) {
    if (program->function_count >= program->function_capacity) {
        program->function_capacity = program->function_capacity == 0 ? 4 : program->function_capacity * 2;
        program->functions = realloc(program->functions, sizeof(Function*) * program->function_capacity);
    }
    program->functions[program->function_count++] = func;
}

static void program_add_type(Program *program, TypeDefinition *type) {
    if (program->type_count >= program->type_capacity) {
        program->type_capacity = program->type_capacity == 0 ? 4 : program->type_capacity * 2;
        program->types = realloc(program->types, sizeof(TypeDefinition*) * program->type_capacity);
    }
    program->types[program->type_count++] = type;
}

static void program_add_import(Program *program, Import *import) {
    if (program->import_count >= program->import_capacity) {
        program->import_capacity = program->import_capacity == 0 ? 4 : program->import_capacity * 2;
        program->imports = realloc(program->imports, sizeof(Import*) * program->import_capacity);
    }
    program->imports[program->import_count++] = import;
}

static Expression* parser_parse_primary(Parser *parser) {
    // Handle built-in functions
    if (parser_is_builtin_function_token(parser->current_token->type)) {
        TokenType builtin_type = parser->current_token->type;
        parser_eat(parser, builtin_type);

        parser_eat(parser, TOKEN_LPAREN);

        // Parse arguments
        Expression **arguments = NULL;
        int argument_count = 0;

        if (parser->current_token->type != TOKEN_RPAREN) {
            int capacity = 2;
            arguments = malloc(sizeof(Expression*) * capacity);

            do {
                if (parser->current_token->type == TOKEN_COMMA) {
                    parser_eat(parser, TOKEN_COMMA);
                }

                Expression *arg = parser_parse_comparison(parser);

                if (argument_count >= capacity) {
                    capacity *= 2;
                    arguments = realloc(arguments, sizeof(Expression*) * capacity);
                }

                arguments[argument_count++] = arg;
            } while (parser->current_token->type == TOKEN_COMMA);
        }

        parser_eat(parser, TOKEN_RPAREN);

        // Create builtin call expression
        Expression *expr = malloc(sizeof(Expression));
        expr->type = EXPR_BUILTIN_CALL;
        expr->data.builtin_call.builtin_type = builtin_type;
        expr->data.builtin_call.arguments = arguments;
        expr->data.builtin_call.argument_count = argument_count;
        return expr;
    }

    if (parser->current_token->type == TOKEN_INTEGER) {
        int value = atoi(parser->current_token->value);
        parser_eat(parser, TOKEN_INTEGER);
        return expression_create_integer(value);
    }

    if (parser->current_token->type == TOKEN_STRING_LITERAL) {
        char *string_value = string_duplicate(parser->current_token->value);

        // Check if this string literal is a known type name
        int is_type = 0;
        Program *prog = parser->current_program;
        if (prog) {
            for (int i = 0; i < prog->type_count; i++) {
                if (strcmp(prog->types[i]->name, string_value) == 0) {
                    is_type = 1;
                    break;
                }
            }
        }

        parser_eat(parser, TOKEN_STRING_LITERAL);

        if (is_type) {
            // This is a type name, create a type expression
            Expression *expr = malloc(sizeof(Expression));
            expr->type = EXPR_TYPE_NAME;
            expr->data.type_name = string_value;
            return expr;
        } else {
            return expression_create_string_literal_owned(string_value);
        }
    }

    if (parser->current_token->type == TOKEN_IDENTIFIER) {
        char *name = string_duplicate(parser->current_token->value);

        // Check if this identifier is a known type name
        int is_type = 0;
        Program *prog = parser->current_program;
        if (prog) {
            for (int i = 0; i < prog->type_count; i++) {
                if (strcmp(prog->types[i]->name, name) == 0) {
                    is_type = 1;
                    break;
                }
            }
        }

        parser_eat(parser, TOKEN_IDENTIFIER);

        // Check if this is a variant constructor (e.g., Circle with radius as 5)
        if (parser->current_token->type == TOKEN_WITH) {
            // Try to determine if this is a variant constructor
            // We need to check if the identifier is a variant name
            char *variant_name = name;
            TypeDefinition *adt_type = NULL;

            // Find the ADT type that contains this variant
            if (prog) {
                for (int i = 0; i < prog->type_count; i++) {
                    if (prog->types[i]->kind == TYPE_KIND_VARIANT) {
                        for (int j = 0; j < prog->types[i]->data.variant_type.variant_count; j++) {
                            if (strcmp(prog->types[i]->data.variant_type.variants[j].name, variant_name) == 0) {
                                adt_type = prog->types[i];
                                break;
                            }
                        }
                        if (adt_type) break;
                    }
                }
            }

            if (adt_type) {
                // This is a variant constructor
                parser_eat(parser, TOKEN_WITH);

                Expression *expr = malloc(sizeof(Expression));
                expr->type = EXPR_VARIANT_CONSTRUCTOR;
                expr->data.variant_constructor.type_name = string_duplicate(adt_type->name);
                expr->data.variant_constructor.variant_name = variant_name;
                expr->data.variant_constructor.field_values = NULL;
                expr->data.variant_constructor.field_count = 0;

                // Find the variant to know what fields to expect
                Variant *variant = NULL;
                for (int i = 0; i < adt_type->data.variant_type.variant_count; i++) {
                    if (strcmp(adt_type->data.variant_type.variants[i].name, variant_name) == 0) {
                        variant = &adt_type->data.variant_type.variants[i];
                        break;
                    }
                }

                if (!variant) {
                    fprintf(stderr, "[PARSER ERROR] Variant '%s' not found in type '%s'\n", variant_name, adt_type->name);
                    exit(1);
                }

                // Parse field values
                if (variant->field_count > 0) {
                    expr->data.variant_constructor.field_values = malloc(sizeof(Expression*) * variant->field_count);

                    for (int i = 0; i < variant->field_count; i++) {
                        // Parse field name
                        if (parser->current_token->type != TOKEN_IDENTIFIER ||
                            strcmp(parser->current_token->value, variant->fields[i].name) != 0) {
                            fprintf(stderr, "[PARSER ERROR] Expected field '%s' at line %d\n",
                                    variant->fields[i].name, parser->current_token->line);
                            exit(1);
                        }
                        parser_eat(parser, TOKEN_IDENTIFIER);
                        parser_eat(parser, TOKEN_AS);

                        // Parse field value expression
                        expr->data.variant_constructor.field_values[i] = parser_parse_expression(parser);
                        expr->data.variant_constructor.field_count++;

                        // Check for "and" between fields
                        if (i < variant->field_count - 1) {
                            if (parser->current_token->type != TOKEN_AND) {
                                fprintf(stderr, "[PARSER ERROR] Expected 'and' between variant fields at line %d\n",
                                        parser->current_token->line);
                                exit(1);
                            }
                            parser_eat(parser, TOKEN_AND);
                        }
                    }
                }

                return expr;
            }
            // If not a variant constructor, fall through to normal identifier handling
        }

        // Check if this is a function call
        if (!is_type && parser->current_token->type == TOKEN_LPAREN) {
            parser_eat(parser, TOKEN_LPAREN);

            // Parse arguments
            Expression **arguments = NULL;
            int argument_count = 0;
            int argument_capacity = 0;

            while (parser->current_token->type != TOKEN_RPAREN && parser->current_token->type != TOKEN_EOF) {
                if (argument_count >= argument_capacity) {
                    argument_capacity = argument_capacity == 0 ? 4 : argument_capacity * 2;
                    arguments = realloc(arguments, sizeof(Expression*) * argument_capacity);
                }
                arguments[argument_count++] = parser_parse_expression(parser);

                if (parser->current_token->type == TOKEN_RPAREN) {
                    break;
                }

                // Expect comma between arguments
                if (parser->current_token->type == TOKEN_COMMA) {
                    parser_eat(parser, TOKEN_COMMA);
                } else {
                    fprintf(stderr, "[PARSER ERROR] Expected ',' or ')' in function arguments at line %d\n", parser->current_token->line);
                    exit(1);
                }
            }

            parser_eat(parser, TOKEN_RPAREN);
            return expression_create_function_call(name, arguments, argument_count);
        } else if (is_type) {
            // This is a type name, create a type expression
            Expression *expr = malloc(sizeof(Expression));
            expr->type = EXPR_TYPE_NAME;
            expr->data.type_name = name;
            return expr;
        } else {
            return expression_create_variable(name);
        }
    }

    fprintf(stderr, "[PARSER ERROR] Expected integer or identifier at line %d\n", parser->current_token->line);
    exit(1);
}

static Expression* parser_parse_expression(Parser *parser) {
    Expression *left = parser_parse_primary(parser);

    // Handle field access first (highest precedence)
    while (parser->current_token->type == TOKEN_DOT) {
        parser_eat(parser, TOKEN_DOT);

        if (parser->current_token->type != TOKEN_IDENTIFIER) {
            fprintf(stderr, "[PARSER ERROR] Expected field name after '.' at line %d\n", parser->current_token->line);
            exit(1);
        }

        char *field_name = string_duplicate(parser->current_token->value);
        parser_eat(parser, TOKEN_IDENTIFIER);

        Expression *field_access = malloc(sizeof(Expression));
        field_access->type = EXPR_FIELD_ACCESS;
        field_access->data.field_access.object = left;
        field_access->data.field_access.field_name = field_name;
        left = field_access;
    }

    // Then handle binary operators
    while (parser->current_token->type == TOKEN_PLUS || parser->current_token->type == TOKEN_MINUS ||
           parser->current_token->type == TOKEN_MULTIPLIED || parser->current_token->type == TOKEN_DIVIDED ||
           parser->current_token->type == TOKEN_MODULO || parser->current_token->type == TOKEN_BIT_AND ||
           parser->current_token->type == TOKEN_BIT_OR || parser->current_token->type == TOKEN_BIT_XOR ||
           parser->current_token->type == TOKEN_BIT_SHIFT_LEFT || parser->current_token->type == TOKEN_BIT_SHIFT_RIGHT) {
        TokenType operator = parser->current_token->type;

        if (operator == TOKEN_MULTIPLIED) {
            parser_eat(parser, TOKEN_MULTIPLIED);
            parser_eat(parser, TOKEN_BY);
        } else if (operator == TOKEN_DIVIDED) {
            parser_eat(parser, TOKEN_DIVIDED);
            parser_eat(parser, TOKEN_BY);
        } else if (operator == TOKEN_MODULO) {
            parser_eat(parser, TOKEN_MODULO);
            parser_eat(parser, TOKEN_BY);
        } else if (operator == TOKEN_BIT_SHIFT_LEFT) {
            parser_eat(parser, TOKEN_BIT_SHIFT_LEFT);
            parser_eat(parser, TOKEN_BY);
        } else if (operator == TOKEN_BIT_SHIFT_RIGHT) {
            parser_eat(parser, TOKEN_BIT_SHIFT_RIGHT);
            parser_eat(parser, TOKEN_BY);
        } else {
            parser_eat(parser, operator);
        }

        Expression *right = parser_parse_primary(parser);

        // Handle field access on the right operand
        while (parser->current_token->type == TOKEN_DOT) {
            parser_eat(parser, TOKEN_DOT);

            if (parser->current_token->type != TOKEN_IDENTIFIER) {
                fprintf(stderr, "[PARSER ERROR] Expected field name after '.' at line %d\n", parser->current_token->line);
                exit(1);
            }

            char *field_name = string_duplicate(parser->current_token->value);
            parser_eat(parser, TOKEN_IDENTIFIER);

            Expression *field_access = malloc(sizeof(Expression));
            field_access->type = EXPR_FIELD_ACCESS;
            field_access->data.field_access.object = right;
            field_access->data.field_access.field_name = field_name;
            right = field_access;
        }

        left = expression_create_binary_op(left, operator, right);
    }

    return left;
}

static Expression* parser_parse_comparison(Parser *parser) {
    Expression *left = parser_parse_expression(parser);

    if (parser->current_token->type == TOKEN_IS) {
        parser_eat(parser, TOKEN_IS);

        TokenType comparison_op;
        if (parser->current_token->type == TOKEN_NOT) {
            parser_eat(parser, TOKEN_NOT);
            parser_eat(parser, TOKEN_EQUAL);
            parser_eat(parser, TOKEN_TO);
            comparison_op = TOKEN_NOT_EQUAL;
        } else if (parser->current_token->type == TOKEN_EQUAL) {
            parser_eat(parser, TOKEN_EQUAL);
            parser_eat(parser, TOKEN_TO);
            comparison_op = TOKEN_EQUAL;
        } else if (parser->current_token->type == TOKEN_LESS) {
            parser_eat(parser, TOKEN_LESS);
            if (parser->current_token->type == TOKEN_THAN) {
                parser_eat(parser, TOKEN_THAN);
                if (parser->current_token->type == TOKEN_OR) {
                    parser_eat(parser, TOKEN_OR);
                    parser_eat(parser, TOKEN_EQUAL);
                    parser_eat(parser, TOKEN_TO);
                    comparison_op = TOKEN_LESS_EQUAL;
                } else {
                    comparison_op = TOKEN_LESS;
                }
            } else {
                fprintf(stderr, "[PARSER ERROR] Expected 'than' after 'less' at line %d\n", parser->current_token->line);
                exit(1);
            }
        } else if (parser->current_token->type == TOKEN_GREATER) {
            parser_eat(parser, TOKEN_GREATER);
            if (parser->current_token->type == TOKEN_THAN) {
                parser_eat(parser, TOKEN_THAN);
                if (parser->current_token->type == TOKEN_OR) {
                    parser_eat(parser, TOKEN_OR);
                    parser_eat(parser, TOKEN_EQUAL);
                    parser_eat(parser, TOKEN_TO);
                    comparison_op = TOKEN_GREATER_EQUAL;
                } else {
                    comparison_op = TOKEN_GREATER;
                }
            } else {
                fprintf(stderr, "[PARSER ERROR] Expected 'than' after 'greater' at line %d\n", parser->current_token->line);
                exit(1);
            }
        } else {
            fprintf(stderr, "[PARSER ERROR] Expected 'equal', 'less', or 'greater' after 'is' at line %d\n", parser->current_token->line);
            exit(1);
        }

        Expression *right = parser_parse_expression(parser);
        return expression_create_comparison(left, comparison_op, right);
    }

    return left;
}

static Statement* parser_parse_let_statement(Parser *parser) {
    parser_eat(parser, TOKEN_LET);

    if (parser->current_token->type != TOKEN_IDENTIFIER) {
        fprintf(stderr, "[PARSER ERROR] Expected identifier after Let at line %d\n", parser->current_token->line);
        exit(1);
    }

    char *var_name = string_duplicate(parser->current_token->value);
    parser_eat(parser, TOKEN_IDENTIFIER);

    parser_eat(parser, TOKEN_BE);

    Expression *expr = parser_parse_expression(parser);

    return statement_create_let(var_name, expr);
}

static Statement* parser_parse_set_statement(Parser *parser) {
    parser_eat(parser, TOKEN_SET);

    // Parse the target expression (could be variable or nested field access)
    Expression *target = parser_parse_expression(parser);

    parser_eat(parser, TOKEN_TO);

    Expression *expr = parser_parse_expression(parser);

    Statement *stmt = statement_create_set(target, expr);
    return stmt;
}

static Statement* parser_parse_return_statement(Parser *parser) {
    parser_eat(parser, TOKEN_RETURN);
    Expression *expr = parser_parse_expression(parser);
    return statement_create_return(expr);
}

static Statement* parser_parse_break_statement(Parser *parser) {
    parser_eat(parser, TOKEN_BREAK);
    return statement_create_break();
}

static Statement* parser_parse_continue_statement(Parser *parser) {
    parser_eat(parser, TOKEN_CONTINUE);
    return statement_create_continue();
}

static Statement* parser_parse_print_statement(Parser *parser) {
    parser_eat(parser, TOKEN_PRINT);
    Expression *expr = parser_parse_expression(parser);
    return statement_create_print(expr);
}

static Statement* parser_parse_inline_assembly_statement(Parser *parser) {
    parser_eat(parser, TOKEN_INLINE);
    parser_eat(parser, TOKEN_ASSEMBLY);
    parser_eat(parser, TOKEN_COLON);

    Statement *stmt = malloc(sizeof(Statement));
    stmt->type = STMT_INLINE_ASSEMBLY;

    // Initialize arrays
    stmt->data.inline_assembly_stmt.assembly_lines = NULL;
    stmt->data.inline_assembly_stmt.assembly_notes = NULL;
    stmt->data.inline_assembly_stmt.assembly_line_count = 0;
    stmt->data.inline_assembly_stmt.output_constraints = NULL;
    stmt->data.inline_assembly_stmt.output_count = 0;
    stmt->data.inline_assembly_stmt.input_constraints = NULL;
    stmt->data.inline_assembly_stmt.input_count = 0;
    stmt->data.inline_assembly_stmt.clobber_list = NULL;
    stmt->data.inline_assembly_stmt.clobber_count = 0;

    // Parse assembly instruction lines
    int capacity = 0;
    while (parser->current_token->type == TOKEN_STRING_LITERAL) {
        // Expand arrays if needed
        if (stmt->data.inline_assembly_stmt.assembly_line_count >= capacity) {
            capacity = (capacity == 0) ? 4 : capacity * 2;
            stmt->data.inline_assembly_stmt.assembly_lines = realloc(
                stmt->data.inline_assembly_stmt.assembly_lines,
                capacity * sizeof(char*)
            );
            stmt->data.inline_assembly_stmt.assembly_notes = realloc(
                stmt->data.inline_assembly_stmt.assembly_notes,
                capacity * sizeof(char*)
            );
        }

        // Parse assembly instruction string
        stmt->data.inline_assembly_stmt.assembly_lines[stmt->data.inline_assembly_stmt.assembly_line_count] =
            string_duplicate(parser->current_token->value);
        parser_advance(parser);

        // Expect "Note:" comment
        if (parser->current_token->type != TOKEN_NOTE) {
            fprintf(stderr, "[PARSER ERROR] Expected Note: comment after assembly instruction at line %d\n",
                    parser->current_token->line);
            exit(1);
        }
        parser_eat(parser, TOKEN_NOTE);
        parser_eat(parser, TOKEN_COLON);

        // Parse note text (could be multiple tokens until newline/next statement)
        // Build note text from multiple identifiers/strings
        char note_buffer[1024] = "";
        int note_length = 0;

        while (parser->current_token->type != TOKEN_STRING_LITERAL &&
               parser->current_token->type != TOKEN_COLON &&
               parser->current_token->type != TOKEN_END &&
               parser->current_token->type != TOKEN_EOF &&
               parser->current_token->type != TOKEN_ASSEMBLY &&
               parser->current_token->type != TOKEN_NOTE) {
            if (note_length > 0) {
                note_buffer[note_length++] = ' '; // Add space between words
            }
            int token_len = strlen(parser->current_token->value);
            if (note_length + token_len < sizeof(note_buffer) - 1) {
                strcpy(note_buffer + note_length, parser->current_token->value);
                note_length += token_len;
            }
            parser_advance(parser);
        }

        if (note_length > 0) {
            stmt->data.inline_assembly_stmt.assembly_notes[stmt->data.inline_assembly_stmt.assembly_line_count] =
                string_duplicate(note_buffer);
        } else {
            stmt->data.inline_assembly_stmt.assembly_notes[stmt->data.inline_assembly_stmt.assembly_line_count] =
                string_duplicate("Assembly instruction");
        }

        stmt->data.inline_assembly_stmt.assembly_line_count++;
    }

    // Parse constraints (optional sections separated by colons)
    // Output constraints
    if (parser->current_token->type == TOKEN_COLON) {
        parser_advance(parser);
        // Parse output constraints until next colon or End
        int out_capacity = 0;
        while (parser->current_token->type != TOKEN_COLON &&
               parser->current_token->type != TOKEN_END &&
               parser->current_token->type != TOKEN_EOF) {

            if (stmt->data.inline_assembly_stmt.output_count >= out_capacity) {
                out_capacity = (out_capacity == 0) ? 4 : out_capacity * 2;
                stmt->data.inline_assembly_stmt.output_constraints = realloc(
                    stmt->data.inline_assembly_stmt.output_constraints,
                    out_capacity * sizeof(char*)
                );
            }

            if (parser->current_token->type == TOKEN_STRING_LITERAL) {
                stmt->data.inline_assembly_stmt.output_constraints[stmt->data.inline_assembly_stmt.output_count] =
                    string_duplicate(parser->current_token->value);
                stmt->data.inline_assembly_stmt.output_count++;
                parser_advance(parser);
            } else {
                parser_advance(parser); // Skip other tokens
            }
        }

        // Input constraints
        if (parser->current_token->type == TOKEN_COLON) {
            parser_advance(parser);
            int in_capacity = 0;
            while (parser->current_token->type != TOKEN_COLON &&
                   parser->current_token->type != TOKEN_END &&
                   parser->current_token->type != TOKEN_EOF) {

                if (stmt->data.inline_assembly_stmt.input_count >= in_capacity) {
                    in_capacity = (in_capacity == 0) ? 4 : in_capacity * 2;
                    stmt->data.inline_assembly_stmt.input_constraints = realloc(
                        stmt->data.inline_assembly_stmt.input_constraints,
                        in_capacity * sizeof(char*)
                    );
                }

                if (parser->current_token->type == TOKEN_STRING_LITERAL) {
                    stmt->data.inline_assembly_stmt.input_constraints[stmt->data.inline_assembly_stmt.input_count] =
                        string_duplicate(parser->current_token->value);
                    stmt->data.inline_assembly_stmt.input_count++;
                    parser_advance(parser);
                } else {
                    parser_advance(parser); // Skip other tokens
                }
            }

            // Clobber list
            if (parser->current_token->type == TOKEN_COLON) {
                parser_advance(parser);
                int clob_capacity = 0;
                while (parser->current_token->type != TOKEN_END &&
                       parser->current_token->type != TOKEN_EOF) {

                    if (stmt->data.inline_assembly_stmt.clobber_count >= clob_capacity) {
                        clob_capacity = (clob_capacity == 0) ? 4 : clob_capacity * 2;
                        stmt->data.inline_assembly_stmt.clobber_list = realloc(
                            stmt->data.inline_assembly_stmt.clobber_list,
                            clob_capacity * sizeof(char*)
                        );
                    }

                    if (parser->current_token->type == TOKEN_STRING_LITERAL ||
                        parser->current_token->type == TOKEN_IDENTIFIER) {
                        stmt->data.inline_assembly_stmt.clobber_list[stmt->data.inline_assembly_stmt.clobber_count] =
                            string_duplicate(parser->current_token->value);
                        stmt->data.inline_assembly_stmt.clobber_count++;
                        parser_advance(parser);
                    } else {
                        parser_advance(parser); // Skip other tokens
                    }
                }
            }
        }
    }

    parser_eat(parser, TOKEN_END);
    parser_eat(parser, TOKEN_ASSEMBLY);

    return stmt;
}

static Statement** parser_parse_statement_block(Parser *parser, int *count) {
    Statement **statements = NULL;
    int capacity = 0;
    *count = 0;

    while (parser->current_token->type != TOKEN_END && parser->current_token->type != TOKEN_OTHERWISE && parser->current_token->type != TOKEN_EOF) {
        Statement *stmt = NULL;

        if (parser->current_token->type == TOKEN_LET) {
            stmt = parser_parse_let_statement(parser);
        } else if (parser->current_token->type == TOKEN_SET) {
            stmt = parser_parse_set_statement(parser);
        } else if (parser->current_token->type == TOKEN_IF) {
            stmt = parser_parse_if_statement(parser);
        } else if (parser->current_token->type == TOKEN_WHILE) {
            stmt = parser_parse_while_statement(parser);
        } else if (parser->current_token->type == TOKEN_MATCH) {
            stmt = parser_parse_match_statement(parser);
        } else if (parser->current_token->type == TOKEN_RETURN) {
            stmt = parser_parse_return_statement(parser);
        } else if (parser->current_token->type == TOKEN_BREAK) {
            stmt = parser_parse_break_statement(parser);
        } else if (parser->current_token->type == TOKEN_CONTINUE) {
            stmt = parser_parse_continue_statement(parser);
        } else if (parser->current_token->type == TOKEN_PRINT) {
            stmt = parser_parse_print_statement(parser);
        } else if (parser->current_token->type == TOKEN_INLINE) {
            stmt = parser_parse_inline_assembly_statement(parser);
        } else if (parser->current_token->type == TOKEN_IDENTIFIER) {
            // Try to parse as expression (could be a function call)
            Expression *expr = parser_parse_expression(parser);
            // Only function calls are valid as standalone statements
            if (expr && expr->type == EXPR_FUNCTION_CALL) {
                stmt = statement_create_expression(expr);
            } else {
                // Other expressions are not valid as statements
                fprintf(stderr, "[PARSER ERROR] Only function calls can be used as statements at line %d (got expr type %d)\n",
                        parser->current_token->line, expr ? (int)expr->type : -1);
                exit(1);
            }
        } else if (parser_is_builtin_function_token(parser->current_token->type)) {
            // Parse builtin function call as expression statement
            Expression *expr = parser_parse_expression(parser);
            if (expr && expr->type == EXPR_BUILTIN_CALL) {
                stmt = statement_create_expression(expr);
            } else {
                fprintf(stderr, "[PARSER ERROR] Invalid builtin function statement at line %d\n",
                        parser->current_token->line);
                exit(1);
            }
        } else {
            break;
        }

        if (*count >= capacity) {
            capacity = capacity == 0 ? 4 : capacity * 2;
            statements = realloc(statements, sizeof(Statement*) * capacity);
        }
        statements[(*count)++] = stmt;
    }

    return statements;
}

static Statement* parser_parse_if_statement(Parser *parser) {
    parser_eat(parser, TOKEN_IF);
    Expression *condition = parser_parse_comparison(parser);
    parser_eat(parser, TOKEN_COLON);

    int if_body_count;
    Statement **if_body = parser_parse_statement_block(parser, &if_body_count);

    Statement **else_body = NULL;
    int else_body_count = 0;

    // Handle elif/else chains
    while (parser->current_token->type == TOKEN_OTHERWISE) {
        parser_eat(parser, TOKEN_OTHERWISE);

        // Check if this is "Otherwise If" (elif)
        if (parser->current_token->type == TOKEN_IF) {
            // Parse elif condition and body, create nested if statement
            parser_eat(parser, TOKEN_IF);
            Expression *elif_condition = parser_parse_comparison(parser);
            parser_eat(parser, TOKEN_COLON);

            int elif_body_count;
            Statement **elif_body = parser_parse_statement_block(parser, &elif_body_count);

            // Create a nested if statement for the elif
            Statement *elif_stmt = statement_create_if(elif_condition, elif_body, elif_body_count, NULL, 0);

            if (else_body == NULL) {
                // First elif - create else body
                else_body = malloc(sizeof(Statement*));
                else_body[0] = elif_stmt;
                else_body_count = 1;
            } else {
                // Chain elif to the previous else clause
                // The last statement in else_body should be an if statement
                Statement *last_if = else_body[else_body_count - 1];
                last_if->data.if_stmt.else_body = malloc(sizeof(Statement*));
                last_if->data.if_stmt.else_body[0] = elif_stmt;
                last_if->data.if_stmt.else_body_count = 1;
            }
        } else {
            // Regular "Otherwise" clause - this ends the elif chain
            parser_eat(parser, TOKEN_COLON);
            Statement **final_else_body = parser_parse_statement_block(parser, &else_body_count);

            if (else_body == NULL) {
                // No previous elifs, this is a simple else
                else_body = final_else_body;
            } else {
                // Attach to the last elif
                Statement *last_if = else_body[else_body_count - 1];
                // Find the deepest nested if statement
                while (last_if->data.if_stmt.else_body != NULL && last_if->data.if_stmt.else_body_count == 1 &&
                       last_if->data.if_stmt.else_body[0]->type == STMT_IF) {
                    last_if = last_if->data.if_stmt.else_body[0];
                }
                last_if->data.if_stmt.else_body = final_else_body;
                last_if->data.if_stmt.else_body_count = else_body_count;
            }
            break; // Final else clause ends the chain
        }
    }

    parser_eat(parser, TOKEN_END);
    parser_eat(parser, TOKEN_IF);

    return statement_create_if(condition, if_body, if_body_count, else_body, else_body_count);
}

static Statement* parser_parse_while_statement(Parser *parser) {
    parser_eat(parser, TOKEN_WHILE);
    Expression *condition = parser_parse_comparison(parser);
    parser_eat(parser, TOKEN_COLON);

    int body_count;
    Statement **body = parser_parse_statement_block(parser, &body_count);

    parser_eat(parser, TOKEN_END);
    parser_eat(parser, TOKEN_WHILE);

    return statement_create_while(condition, body, body_count);
}

static Statement* parser_parse_match_statement(Parser *parser) {
    // Parse: Match expression:
    parser_eat(parser, TOKEN_MATCH);

    Expression *expression = parser_parse_expression(parser);
    parser_eat(parser, TOKEN_COLON);

    Statement *stmt = malloc(sizeof(Statement));
    stmt->type = STMT_MATCH;
    stmt->data.match_stmt.expression = expression;
    stmt->data.match_stmt.cases = NULL;
    stmt->data.match_stmt.case_count = 0;

    // Parse match cases
    while (parser->current_token->type == TOKEN_WHEN) {
        parser_eat(parser, TOKEN_WHEN);

        // Parse variant name
        if (parser->current_token->type != TOKEN_IDENTIFIER) {
            fprintf(stderr, "[PARSER ERROR] Expected variant name after 'When' at line %d\n",
                    parser->current_token->line);
            exit(1);
        }

        char *variant_name = string_duplicate(parser->current_token->value);
        parser_eat(parser, TOKEN_IDENTIFIER);

        // Parse optional field bindings
        char **field_names = NULL;
        int field_count = 0;

        if (parser->current_token->type == TOKEN_WITH) {
            parser_eat(parser, TOKEN_WITH);

            // Count fields for this variant (we need to look it up)
            // For now, parse field bindings: field1 as var1 and field2 as var2...
            field_names = malloc(sizeof(char*) * 10); // Max 10 fields for now

            while (1) {
                // Parse field name
                if (parser->current_token->type != TOKEN_IDENTIFIER) {
                    fprintf(stderr, "[PARSER ERROR] Expected field name in match case at line %d\n",
                            parser->current_token->line);
                    exit(1);
                }
                parser_eat(parser, TOKEN_IDENTIFIER); // Skip actual field name
                parser_eat(parser, TOKEN_AS);

                // Parse binding variable
                if (parser->current_token->type != TOKEN_IDENTIFIER) {
                    fprintf(stderr, "[PARSER ERROR] Expected binding variable name at line %d\n",
                            parser->current_token->line);
                    exit(1);
                }

                field_names[field_count++] = string_duplicate(parser->current_token->value);
                parser_eat(parser, TOKEN_IDENTIFIER);

                // Check for "and" to continue with more fields
                if (parser->current_token->type == TOKEN_AND) {
                    parser_eat(parser, TOKEN_AND);
                } else {
                    break;
                }
            }
        }

        parser_eat(parser, TOKEN_COLON);

        // Parse case body
        int body_count = 0;
        Statement **body = parser_parse_statement_block(parser, &body_count);

        parser_eat(parser, TOKEN_END);
        parser_eat(parser, TOKEN_WHEN);

        // Add match case
        stmt->data.match_stmt.case_count++;
        stmt->data.match_stmt.cases = realloc(stmt->data.match_stmt.cases,
                                              sizeof(MatchCase) * stmt->data.match_stmt.case_count);
        MatchCase *match_case = &stmt->data.match_stmt.cases[stmt->data.match_stmt.case_count - 1];
        match_case->variant_name = variant_name;
        match_case->field_names = field_names;
        match_case->field_count = field_count;
        match_case->body = body;
        match_case->body_count = body_count;
    }

    parser_eat(parser, TOKEN_END);
    parser_eat(parser, TOKEN_MATCH);

    return stmt;
}

// Calculate size of a type in bytes
static int calculate_type_size(const char *type_name, Program *program) {
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

    // Unknown type - default to 8 bytes and warn
    fprintf(stderr, "[PARSER WARNING] Unknown type '%s', defaulting to 8 bytes\n", type_name);
    return 8;
}

static TypeDefinition* parser_parse_type_definition(Parser *parser) {
    // Parse: Type called "name": OR Type Name is
    parser_eat(parser, TOKEN_TYPE);

    TypeDefinition *type = malloc(sizeof(TypeDefinition));

    // Check for "called" syntax for struct types
    if (parser->current_token->type == TOKEN_CALLED) {
        parser_eat(parser, TOKEN_CALLED);

        if (parser->current_token->type != TOKEN_STRING_LITERAL) {
            fprintf(stderr, "[PARSER ERROR] Expected type name at line %d\n", parser->current_token->line);
            exit(1);
        }

        type->name = string_duplicate(parser->current_token->value);
        parser_eat(parser, TOKEN_STRING_LITERAL);
        parser_eat(parser, TOKEN_COLON);

        // This is a struct type
        type->kind = TYPE_KIND_STRUCT;
        type->data.struct_type.fields = NULL;
        type->data.struct_type.field_count = 0;
        int current_offset = 0;

        // Parse field declarations until "End Type"
        while (parser->current_token->type != TOKEN_END) {
            // Parse field: name as Type
            if (parser->current_token->type != TOKEN_IDENTIFIER) {
                fprintf(stderr, "[PARSER ERROR] Expected field name at line %d (got token type %d)\n",
                        parser->current_token->line, parser->current_token->type);
                exit(1);
            }

            char *field_name = string_duplicate(parser->current_token->value);
            parser_eat(parser, TOKEN_IDENTIFIER);
            parser_eat(parser, TOKEN_AS);

            if (parser->current_token->type != TOKEN_INTEGER_TYPE &&
                parser->current_token->type != TOKEN_STRING_TYPE &&
                parser->current_token->type != TOKEN_CHARACTER_TYPE &&
                parser->current_token->type != TOKEN_IDENTIFIER) {
                fprintf(stderr, "[PARSER ERROR] Expected field type at line %d\n", parser->current_token->line);
                exit(1);
            }

            char *field_type = string_duplicate(parser->current_token->value);
            if (parser->current_token->type == TOKEN_INTEGER_TYPE) {
                parser_eat(parser, TOKEN_INTEGER_TYPE);
            } else if (parser->current_token->type == TOKEN_STRING_TYPE) {
                parser_eat(parser, TOKEN_STRING_TYPE);
            } else if (parser->current_token->type == TOKEN_CHARACTER_TYPE) {
                parser_eat(parser, TOKEN_CHARACTER_TYPE);
            } else {
                parser_eat(parser, TOKEN_IDENTIFIER);
            }

            // Check for comma after field declaration
            // The comma is optional for the last field
            if (parser->current_token->type == TOKEN_COMMA) {
                parser_eat(parser, TOKEN_COMMA);
            }

            // Add field to type
            type->data.struct_type.field_count++;
            type->data.struct_type.fields = realloc(type->data.struct_type.fields,
                                                     sizeof(TypeField) * type->data.struct_type.field_count);
            TypeField *field = &type->data.struct_type.fields[type->data.struct_type.field_count - 1];
            field->name = field_name;
            field->type = field_type;
            field->offset = current_offset;

            // Calculate field size based on type
            field->size = calculate_type_size(field_type, parser->current_program);
            current_offset += field->size;
        }

        type->size = current_offset;

        parser_eat(parser, TOKEN_END);
        parser_eat(parser, TOKEN_TYPE);
    }
    // Check for variant syntax: Type Name is | Variant1 ...
    else if (parser->current_token->type == TOKEN_IDENTIFIER) {
        type->name = string_duplicate(parser->current_token->value);
        parser_eat(parser, TOKEN_IDENTIFIER);
        parser_eat(parser, TOKEN_IS);

        // This is a variant type
        type->kind = TYPE_KIND_VARIANT;
        type->data.variant_type.variants = NULL;
        type->data.variant_type.variant_count = 0;

        // Parse variants
        while (parser->current_token->type == TOKEN_PIPE) {
            parser_eat(parser, TOKEN_PIPE);

            // Parse variant name
            if (parser->current_token->type != TOKEN_IDENTIFIER) {
                fprintf(stderr, "[PARSER ERROR] Expected variant name at line %d\n", parser->current_token->line);
                exit(1);
            }

            // Add variant
            type->data.variant_type.variant_count++;
            type->data.variant_type.variants = realloc(type->data.variant_type.variants,
                                                       sizeof(Variant) * type->data.variant_type.variant_count);
            Variant *variant = &type->data.variant_type.variants[type->data.variant_type.variant_count - 1];
            variant->name = string_duplicate(parser->current_token->value);
            variant->fields = NULL;
            variant->field_count = 0;
            variant->tag = type->data.variant_type.variant_count - 1; // Tag is 0-based index

            parser_eat(parser, TOKEN_IDENTIFIER);

            // Parse optional variant fields
            if (parser->current_token->type == TOKEN_WITH) {
                parser_eat(parser, TOKEN_WITH);

                int field_offset = 8; // Start after tag (8 bytes for tag)

                // Parse fields: field1 as Type1 and field2 as Type2...
                while (1) {
                    // Parse field name
                    if (parser->current_token->type != TOKEN_IDENTIFIER) {
                        fprintf(stderr, "[PARSER ERROR] Expected field name in variant at line %d\n",
                                parser->current_token->line);
                        exit(1);
                    }

                    char *field_name = string_duplicate(parser->current_token->value);
                    parser_eat(parser, TOKEN_IDENTIFIER);
                    parser_eat(parser, TOKEN_AS);

                    // Parse field type
                    if (parser->current_token->type != TOKEN_INTEGER_TYPE &&
                        parser->current_token->type != TOKEN_STRING_TYPE &&
                        parser->current_token->type != TOKEN_CHARACTER_TYPE &&
                        parser->current_token->type != TOKEN_IDENTIFIER) {
                        fprintf(stderr, "[PARSER ERROR] Expected field type at line %d\n",
                                parser->current_token->line);
                        exit(1);
                    }

                    char *field_type = string_duplicate(parser->current_token->value);
                    if (parser->current_token->type == TOKEN_INTEGER_TYPE) {
                        parser_eat(parser, TOKEN_INTEGER_TYPE);
                    } else if (parser->current_token->type == TOKEN_STRING_TYPE) {
                        parser_eat(parser, TOKEN_STRING_TYPE);
                    } else if (parser->current_token->type == TOKEN_CHARACTER_TYPE) {
                        parser_eat(parser, TOKEN_CHARACTER_TYPE);
                    } else {
                        parser_eat(parser, TOKEN_IDENTIFIER);
                    }

                    // Add field to variant
                    variant->field_count++;
                    variant->fields = realloc(variant->fields, sizeof(TypeField) * variant->field_count);
                    TypeField *field = &variant->fields[variant->field_count - 1];
                    field->name = field_name;
                    field->type = field_type;
                    field->offset = field_offset;
                    field->size = calculate_type_size(field_type, parser->current_program);
                    field_offset += field->size;

                    // Check for "and" to continue with more fields
                    if (parser->current_token->type == TOKEN_AND) {
                        parser_eat(parser, TOKEN_AND);
                    } else {
                        break;
                    }
                }
            }
        }

        // Calculate max size needed for any variant
        type->size = 8; // At least tag size
        for (int i = 0; i < type->data.variant_type.variant_count; i++) {
            int variant_size = 8; // Tag size
            for (int j = 0; j < type->data.variant_type.variants[i].field_count; j++) {
                variant_size += type->data.variant_type.variants[i].fields[j].size;
            }
            if (variant_size > type->size) {
                type->size = variant_size;
            }
        }
    } else {
        fprintf(stderr, "[PARSER ERROR] Expected 'called' or type name after 'Type' at line %d\n",
                parser->current_token->line);
        exit(1);
    }

    return type;
}

static Function* parser_parse_function(Parser *parser) {
    // Parse: Process called "name" [that takes param as Type] returns Type:
    parser_eat(parser, TOKEN_PROCESS);
    parser_eat(parser, TOKEN_CALLED);

    if (parser->current_token->type != TOKEN_STRING_LITERAL) {
        fprintf(stderr, "[PARSER ERROR] Expected function name string literal at line %d\n", parser->current_token->line);
        exit(1);
    }

    char *func_name = string_duplicate(parser->current_token->value);
    parser_eat(parser, TOKEN_STRING_LITERAL);

    Function *func = function_create(func_name, "Integer"); // Default return type

    // Check for parameters: "takes param as Type" or "takes x as Type, y as Type"
    if (parser->current_token->type == TOKEN_TAKES) {
        parser_eat(parser, TOKEN_TAKES);

        // Parse first parameter
        if (parser->current_token->type != TOKEN_IDENTIFIER) {
            fprintf(stderr, "[PARSER ERROR] Expected parameter name at line %d\n", parser->current_token->line);
            exit(1);
        }

        char *param_name = string_duplicate(parser->current_token->value);
        parser_eat(parser, TOKEN_IDENTIFIER);
        parser_eat(parser, TOKEN_AS);

        if (parser->current_token->type != TOKEN_INTEGER_TYPE &&
            parser->current_token->type != TOKEN_STRING_TYPE &&
            parser->current_token->type != TOKEN_CHARACTER_TYPE) {
            fprintf(stderr, "[PARSER ERROR] Expected parameter type at line %d\n", parser->current_token->line);
            exit(1);
        }

        char *param_type = string_duplicate(parser->current_token->value);
        if (parser->current_token->type == TOKEN_INTEGER_TYPE) {
            parser_eat(parser, TOKEN_INTEGER_TYPE);
        } else if (parser->current_token->type == TOKEN_STRING_TYPE) {
            parser_eat(parser, TOKEN_STRING_TYPE);
        } else if (parser->current_token->type == TOKEN_CHARACTER_TYPE) {
            parser_eat(parser, TOKEN_CHARACTER_TYPE);
        }

        function_add_parameter(func, param_name, param_type);
        free(param_name);
        free(param_type);

        // Parse additional parameters separated by commas
        while (parser->current_token->type == TOKEN_COMMA) {
            parser_eat(parser, TOKEN_COMMA);

            if (parser->current_token->type != TOKEN_IDENTIFIER) {
                fprintf(stderr, "[PARSER ERROR] Expected parameter name after comma at line %d\n", parser->current_token->line);
                exit(1);
            }

            param_name = string_duplicate(parser->current_token->value);
            parser_eat(parser, TOKEN_IDENTIFIER);
            parser_eat(parser, TOKEN_AS);

            if (parser->current_token->type != TOKEN_INTEGER_TYPE &&
                parser->current_token->type != TOKEN_STRING_TYPE &&
                parser->current_token->type != TOKEN_CHARACTER_TYPE) {
                fprintf(stderr, "[PARSER ERROR] Expected parameter type at line %d\n", parser->current_token->line);
                exit(1);
            }

            param_type = string_duplicate(parser->current_token->value);
            if (parser->current_token->type == TOKEN_INTEGER_TYPE) {
                parser_eat(parser, TOKEN_INTEGER_TYPE);
            } else if (parser->current_token->type == TOKEN_STRING_TYPE) {
                parser_eat(parser, TOKEN_STRING_TYPE);
            } else if (parser->current_token->type == TOKEN_CHARACTER_TYPE) {
                parser_eat(parser, TOKEN_CHARACTER_TYPE);
            }

            function_add_parameter(func, param_name, param_type);
            free(param_name);
            free(param_type);
        }
    }

    parser_eat(parser, TOKEN_RETURNS);

    // Handle different return types
    if (parser->current_token->type == TOKEN_INTEGER_TYPE) {
        parser_eat(parser, TOKEN_INTEGER_TYPE);
    } else if (parser->current_token->type == TOKEN_STRING_TYPE) {
        parser_eat(parser, TOKEN_STRING_TYPE);
    } else if (parser->current_token->type == TOKEN_CHARACTER_TYPE) {
        parser_eat(parser, TOKEN_CHARACTER_TYPE);
    } else if (parser->current_token->type == TOKEN_IDENTIFIER) {
        // Custom type
        parser_eat(parser, TOKEN_IDENTIFIER);
    } else {
        fprintf(stderr, "[PARSER ERROR] Expected return type at line %d\n", parser->current_token->line);
        exit(1);
    }

    parser_eat(parser, TOKEN_COLON);

    // Parse function body statements
    while (parser->current_token->type != TOKEN_RETURN && parser->current_token->type != TOKEN_END && parser->current_token->type != TOKEN_EOF) {
        Statement *stmt = NULL;

        if (parser->current_token->type == TOKEN_LET) {
            stmt = parser_parse_let_statement(parser);
        } else if (parser->current_token->type == TOKEN_SET) {
            stmt = parser_parse_set_statement(parser);
        } else if (parser->current_token->type == TOKEN_IF) {
            stmt = parser_parse_if_statement(parser);
        } else if (parser->current_token->type == TOKEN_WHILE) {
            stmt = parser_parse_while_statement(parser);
        } else if (parser->current_token->type == TOKEN_MATCH) {
            stmt = parser_parse_match_statement(parser);
        } else if (parser->current_token->type == TOKEN_PRINT) {
            stmt = parser_parse_print_statement(parser);
        } else if (parser->current_token->type == TOKEN_INLINE) {
            stmt = parser_parse_inline_assembly_statement(parser);
        } else if (parser->current_token->type == TOKEN_IDENTIFIER) {
            // Try to parse as expression (could be a function call)
            Expression *expr = parser_parse_expression(parser);
            // Only function calls are valid as standalone statements
            if (expr && expr->type == EXPR_FUNCTION_CALL) {
                stmt = statement_create_expression(expr);
            } else {
                // Other expressions are not valid as statements
                fprintf(stderr, "[PARSER ERROR] Only function calls can be used as statements at line %d\n",
                        parser->current_token->line);
                exit(1);
            }
        } else if (parser_is_builtin_function_token(parser->current_token->type)) {
            // Parse builtin function call as expression statement
            Expression *expr = parser_parse_expression(parser);
            if (expr && expr->type == EXPR_BUILTIN_CALL) {
                stmt = statement_create_expression(expr);
            } else {
                fprintf(stderr, "[PARSER ERROR] Invalid builtin function statement at line %d\n",
                        parser->current_token->line);
                exit(1);
            }
        } else {
            fprintf(stderr, "[PARSER ERROR] Unexpected token '%s' (type %d) in function body at line %d\n",
                    parser->current_token->value, parser->current_token->type, parser->current_token->line);
            exit(1);
        }

        function_add_statement(func, stmt);
    }

    // Parse Return statement
    if (parser->current_token->type == TOKEN_RETURN) {
        Statement *return_stmt = parser_parse_return_statement(parser);
        function_add_statement(func, return_stmt);
    }

    // Parse: End Process
    parser_eat(parser, TOKEN_END);
    parser_eat(parser, TOKEN_PROCESS);

    free(func_name);
    return func;
}

Parser* parser_create(Lexer *lexer) {
    Parser *parser = malloc(sizeof(Parser));
    parser->lexer = lexer;
    parser->current_token = lexer_next_token(lexer);
    parser->current_program = NULL;
    return parser;
}

void parser_destroy(Parser *parser) {
    if (parser) {
        token_destroy(parser->current_token);
        free(parser);
    }
}

Program* parser_parse_program(Parser *parser) {
    Program *program = program_create();
    parser->current_program = program;  // Set current program for type lookups

    // Parse imports, type definitions and functions until EOF
    while (parser->current_token->type != TOKEN_EOF) {
        if (parser->current_token->type == TOKEN_IMPORT) {
            // Parse Import statement
            parser_eat(parser, TOKEN_IMPORT);

            // Get filename (must be a string literal)
            if (parser->current_token->type != TOKEN_STRING_LITERAL) {
                fprintf(stderr, "[PARSER ERROR] Expected string literal after Import at line %d\n",
                        parser->current_token->line);
                exit(1);
            }
            char *filename = string_duplicate(parser->current_token->value);
            parser_eat(parser, TOKEN_STRING_LITERAL);

            // Expect "as"
            parser_eat(parser, TOKEN_AS);

            // Get module name
            if (parser->current_token->type != TOKEN_IDENTIFIER) {
                fprintf(stderr, "[PARSER ERROR] Expected module name after 'as' at line %d\n",
                        parser->current_token->line);
                exit(1);
            }
            char *module_name = string_duplicate(parser->current_token->value);
            parser_eat(parser, TOKEN_IDENTIFIER);

            // Create and add import
            Import *import = malloc(sizeof(Import));
            import->filename = filename;
            import->module_name = module_name;
            program_add_import(program, import);
        } else if (parser->current_token->type == TOKEN_TYPE) {
            TypeDefinition *type = parser_parse_type_definition(parser);
            program_add_type(program, type);
        } else if (parser->current_token->type == TOKEN_PROCESS) {
            Function *func = parser_parse_function(parser);
            program_add_function(program, func);
        } else {
            fprintf(stderr, "[PARSER ERROR] Unexpected token at top level at line %d\n",
                    parser->current_token->line);
            exit(1);
        }
    }

    // Don't require EOF to be explicitly parsed, just verify we're at the end
    return program;
}

void expression_destroy(Expression *expr) {
    if (expr) {
        if (expr->type == EXPR_VARIABLE) {
            free(expr->data.variable_name);
        } else if (expr->type == EXPR_BINARY_OP) {
            expression_destroy(expr->data.binary_op.left);
            expression_destroy(expr->data.binary_op.right);
        } else if (expr->type == EXPR_COMPARISON) {
            expression_destroy(expr->data.comparison.left);
            expression_destroy(expr->data.comparison.right);
        } else if (expr->type == EXPR_FUNCTION_CALL) {
            free(expr->data.function_call.function_name);
            for (int i = 0; i < expr->data.function_call.argument_count; i++) {
                expression_destroy(expr->data.function_call.arguments[i]);
            }
            free(expr->data.function_call.arguments);
        } else if (expr->type == EXPR_STRING_LITERAL) {
            free(expr->data.string_literal);
        } else if (expr->type == EXPR_FIELD_ACCESS) {
            expression_destroy(expr->data.field_access.object);
            free(expr->data.field_access.field_name);
        } else if (expr->type == EXPR_TYPE_NAME) {
            free(expr->data.type_name);
        } else if (expr->type == EXPR_BUILTIN_CALL) {
            for (int i = 0; i < expr->data.builtin_call.argument_count; i++) {
                expression_destroy(expr->data.builtin_call.arguments[i]);
            }
            free(expr->data.builtin_call.arguments);
        } else if (expr->type == EXPR_VARIANT_CONSTRUCTOR) {
            free(expr->data.variant_constructor.type_name);
            free(expr->data.variant_constructor.variant_name);
            for (int i = 0; i < expr->data.variant_constructor.field_count; i++) {
                expression_destroy(expr->data.variant_constructor.field_values[i]);
            }
            free(expr->data.variant_constructor.field_values);
        }
        free(expr);
    }
}

static void statement_destroy(Statement *stmt) {
    if (stmt) {
        switch (stmt->type) {
            case STMT_LET:
                free(stmt->data.let_stmt.variable_name);
                expression_destroy(stmt->data.let_stmt.expression);
                break;
            case STMT_SET:
                expression_destroy(stmt->data.set_stmt.target);
                expression_destroy(stmt->data.set_stmt.expression);
                break;
            case STMT_RETURN:
                expression_destroy(stmt->data.return_stmt.expression);
                break;
            case STMT_IF:
                expression_destroy(stmt->data.if_stmt.condition);
                for (int i = 0; i < stmt->data.if_stmt.if_body_count; i++) {
                    statement_destroy(stmt->data.if_stmt.if_body[i]);
                }
                free(stmt->data.if_stmt.if_body);
                for (int i = 0; i < stmt->data.if_stmt.else_body_count; i++) {
                    statement_destroy(stmt->data.if_stmt.else_body[i]);
                }
                free(stmt->data.if_stmt.else_body);
                break;
            case STMT_WHILE:
                expression_destroy(stmt->data.while_stmt.condition);
                for (int i = 0; i < stmt->data.while_stmt.body_count; i++) {
                    statement_destroy(stmt->data.while_stmt.body[i]);
                }
                free(stmt->data.while_stmt.body);
                break;
            case STMT_PRINT:
                expression_destroy(stmt->data.print_stmt.expression);
                break;
            case STMT_EXPRESSION:
                expression_destroy(stmt->data.expr_stmt.expression);
                break;
            case STMT_IMPORT:
                free(stmt->data.import_stmt.filename);
                free(stmt->data.import_stmt.module_name);
                break;
            case STMT_MATCH:
                expression_destroy(stmt->data.match_stmt.expression);
                for (int i = 0; i < stmt->data.match_stmt.case_count; i++) {
                    MatchCase *match_case = &stmt->data.match_stmt.cases[i];
                    free(match_case->variant_name);
                    for (int j = 0; j < match_case->field_count; j++) {
                        free(match_case->field_names[j]);
                    }
                    free(match_case->field_names);
                    for (int j = 0; j < match_case->body_count; j++) {
                        statement_destroy(match_case->body[j]);
                    }
                    free(match_case->body);
                }
                free(stmt->data.match_stmt.cases);
                break;
            case STMT_BREAK:
                // Break statements have no allocated data to free
                break;
            case STMT_CONTINUE:
                // Continue statements have no allocated data to free
                break;
            case STMT_INLINE_ASSEMBLY:
                // Free assembly instruction lines
                for (int i = 0; i < stmt->data.inline_assembly_stmt.assembly_line_count; i++) {
                    free(stmt->data.inline_assembly_stmt.assembly_lines[i]);
                    free(stmt->data.inline_assembly_stmt.assembly_notes[i]);
                }
                free(stmt->data.inline_assembly_stmt.assembly_lines);
                free(stmt->data.inline_assembly_stmt.assembly_notes);

                // Free output constraints
                for (int i = 0; i < stmt->data.inline_assembly_stmt.output_count; i++) {
                    free(stmt->data.inline_assembly_stmt.output_constraints[i]);
                }
                free(stmt->data.inline_assembly_stmt.output_constraints);

                // Free input constraints
                for (int i = 0; i < stmt->data.inline_assembly_stmt.input_count; i++) {
                    free(stmt->data.inline_assembly_stmt.input_constraints[i]);
                }
                free(stmt->data.inline_assembly_stmt.input_constraints);

                // Free clobber list
                for (int i = 0; i < stmt->data.inline_assembly_stmt.clobber_count; i++) {
                    free(stmt->data.inline_assembly_stmt.clobber_list[i]);
                }
                free(stmt->data.inline_assembly_stmt.clobber_list);
                break;
        }
        free(stmt);
    }
}

static void function_destroy(Function *func) {
    if (func) {
        free(func->name);
        free(func->return_type);
        for (int i = 0; i < func->parameter_count; i++) {
            free(func->parameters[i].name);
            free(func->parameters[i].type);
        }
        free(func->parameters);
        for (int i = 0; i < func->statement_count; i++) {
            statement_destroy(func->statements[i]);
        }
        free(func->statements);
        free(func);
    }
}

static void type_destroy(TypeDefinition *type) {
    if (type) {
        free(type->name);
        if (type->kind == TYPE_KIND_STRUCT) {
            for (int i = 0; i < type->data.struct_type.field_count; i++) {
                free(type->data.struct_type.fields[i].name);
                free(type->data.struct_type.fields[i].type);
            }
            free(type->data.struct_type.fields);
        } else if (type->kind == TYPE_KIND_VARIANT) {
            for (int i = 0; i < type->data.variant_type.variant_count; i++) {
                Variant *variant = &type->data.variant_type.variants[i];
                free(variant->name);
                for (int j = 0; j < variant->field_count; j++) {
                    free(variant->fields[j].name);
                    free(variant->fields[j].type);
                }
                free(variant->fields);
            }
            free(type->data.variant_type.variants);
        }
        free(type);
    }
}

void program_destroy(Program *program) {
    if (program) {
        for (int i = 0; i < program->function_count; i++) {
            function_destroy(program->functions[i]);
        }
        free(program->functions);
        for (int i = 0; i < program->type_count; i++) {
            type_destroy(program->types[i]);
        }
        free(program->types);
        for (int i = 0; i < program->import_count; i++) {
            free(program->imports[i]->filename);
            free(program->imports[i]->module_name);
            free(program->imports[i]);
        }
        free(program->imports);
        free(program);
    }
}