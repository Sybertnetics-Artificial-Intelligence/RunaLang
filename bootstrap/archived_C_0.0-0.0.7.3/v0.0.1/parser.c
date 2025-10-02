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

static char* string_duplicate(const char *str) {
    if (!str) return NULL;
    int len = strlen(str);
    char *dup = malloc(len + 1);
    strcpy(dup, str);
    return dup;
}

static void parser_eat(Parser *parser, TokenType expected_type) {
    if (parser->current_token->type == expected_type) {
        token_destroy(parser->current_token);
        parser->current_token = lexer_next_token(parser->lexer);
    } else {
        fprintf(stderr, "Parser error: Expected token type %d, got %d at line %d\n",
                expected_type, parser->current_token->type, parser->current_token->line);
        exit(1);
    }
}

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

static Statement* statement_create_let(const char *var_name, Expression *expr) {
    Statement *stmt = malloc(sizeof(Statement));
    stmt->type = STMT_LET;
    stmt->data.let_stmt.variable_name = string_duplicate(var_name);
    stmt->data.let_stmt.expression = expr;
    return stmt;
}

static Statement* statement_create_set(const char *var_name, Expression *expr) {
    Statement *stmt = malloc(sizeof(Statement));
    stmt->type = STMT_SET;
    stmt->data.set_stmt.variable_name = string_duplicate(var_name);
    stmt->data.set_stmt.expression = expr;
    return stmt;
}

static Statement* statement_create_return(Expression *expr) {
    Statement *stmt = malloc(sizeof(Statement));
    stmt->type = STMT_RETURN;
    stmt->data.return_stmt.expression = expr;
    return stmt;
}

static Program* program_create(void) {
    Program *program = malloc(sizeof(Program));
    program->statements = NULL;
    program->statement_count = 0;
    program->statement_capacity = 0;
    return program;
}

static void program_add_statement(Program *program, Statement *stmt) {
    if (program->statement_count >= program->statement_capacity) {
        program->statement_capacity = program->statement_capacity == 0 ? 4 : program->statement_capacity * 2;
        program->statements = realloc(program->statements, sizeof(Statement*) * program->statement_capacity);
    }
    program->statements[program->statement_count++] = stmt;
}

static Expression* parser_parse_primary(Parser *parser) {
    if (parser->current_token->type == TOKEN_INTEGER) {
        int value = atoi(parser->current_token->value);
        parser_eat(parser, TOKEN_INTEGER);
        return expression_create_integer(value);
    }

    if (parser->current_token->type == TOKEN_IDENTIFIER) {
        char *name = string_duplicate(parser->current_token->value);
        parser_eat(parser, TOKEN_IDENTIFIER);
        return expression_create_variable(name);
    }

    fprintf(stderr, "Parser error: Expected integer or identifier at line %d\n", parser->current_token->line);
    exit(1);
}

static Expression* parser_parse_expression(Parser *parser) {
    Expression *left = parser_parse_primary(parser);

    while (parser->current_token->type == TOKEN_PLUS || parser->current_token->type == TOKEN_MINUS) {
        TokenType operator = parser->current_token->type;
        parser_eat(parser, operator);
        Expression *right = parser_parse_primary(parser);
        left = expression_create_binary_op(left, operator, right);
    }

    return left;
}

static Statement* parser_parse_let_statement(Parser *parser) {
    parser_eat(parser, TOKEN_LET);

    if (parser->current_token->type != TOKEN_IDENTIFIER) {
        fprintf(stderr, "Parser error: Expected identifier after Let at line %d\n", parser->current_token->line);
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

    if (parser->current_token->type != TOKEN_IDENTIFIER) {
        fprintf(stderr, "Parser error: Expected identifier after Set at line %d\n", parser->current_token->line);
        exit(1);
    }

    char *var_name = string_duplicate(parser->current_token->value);
    parser_eat(parser, TOKEN_IDENTIFIER);

    parser_eat(parser, TOKEN_TO);

    Expression *expr = parser_parse_expression(parser);

    return statement_create_set(var_name, expr);
}

static Statement* parser_parse_return_statement(Parser *parser) {
    parser_eat(parser, TOKEN_RETURN);
    Expression *expr = parser_parse_expression(parser);
    return statement_create_return(expr);
}

Parser* parser_create(Lexer *lexer) {
    Parser *parser = malloc(sizeof(Parser));
    parser->lexer = lexer;
    parser->current_token = lexer_next_token(lexer);
    return parser;
}

void parser_destroy(Parser *parser) {
    if (parser) {
        token_destroy(parser->current_token);
        free(parser);
    }
}

Program* parser_parse_program(Parser *parser) {
    // Parse: Process called "main" returns Integer:
    parser_eat(parser, TOKEN_PROCESS);
    parser_eat(parser, TOKEN_CALLED);
    parser_eat(parser, TOKEN_STRING_LITERAL); // "main"
    parser_eat(parser, TOKEN_RETURNS);
    parser_eat(parser, TOKEN_INTEGER_TYPE);
    parser_eat(parser, TOKEN_COLON);

    Program *program = program_create();

    // Parse statements until Return
    while (parser->current_token->type != TOKEN_RETURN && parser->current_token->type != TOKEN_EOF) {
        Statement *stmt = NULL;

        if (parser->current_token->type == TOKEN_LET) {
            stmt = parser_parse_let_statement(parser);
        } else if (parser->current_token->type == TOKEN_SET) {
            stmt = parser_parse_set_statement(parser);
        } else {
            fprintf(stderr, "Parser error: Unexpected token at line %d\n", parser->current_token->line);
            exit(1);
        }

        program_add_statement(program, stmt);
    }

    // Parse Return statement
    Statement *return_stmt = parser_parse_return_statement(parser);
    program_add_statement(program, return_stmt);

    // Parse: End Process
    parser_eat(parser, TOKEN_END);
    parser_eat(parser, TOKEN_PROCESS);

    parser_eat(parser, TOKEN_EOF);

    return program;
}

void expression_destroy(Expression *expr) {
    if (expr) {
        if (expr->type == EXPR_VARIABLE) {
            free(expr->data.variable_name);
        } else if (expr->type == EXPR_BINARY_OP) {
            expression_destroy(expr->data.binary_op.left);
            expression_destroy(expr->data.binary_op.right);
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
                free(stmt->data.set_stmt.variable_name);
                expression_destroy(stmt->data.set_stmt.expression);
                break;
            case STMT_RETURN:
                expression_destroy(stmt->data.return_stmt.expression);
                break;
        }
        free(stmt);
    }
}

void program_destroy(Program *program) {
    if (program) {
        for (int i = 0; i < program->statement_count; i++) {
            statement_destroy(program->statements[i]);
        }
        free(program->statements);
        free(program);
    }
}