#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "parser.h"

// Forward declarations
static Statement* parser_parse_if_statement(Parser *parser);
static Statement* parser_parse_while_statement(Parser *parser);

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

static Expression* expression_create_comparison(Expression *left, TokenType comparison_op, Expression *right) {
    Expression *expr = malloc(sizeof(Expression));
    expr->type = EXPR_COMPARISON;
    expr->data.comparison.left = left;
    expr->data.comparison.right = right;
    expr->data.comparison.comparison_op = comparison_op;
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

static Expression* parser_parse_comparison(Parser *parser) {
    Expression *left = parser_parse_expression(parser);

    if (parser->current_token->type == TOKEN_IS) {
        parser_eat(parser, TOKEN_IS);

        TokenType comparison_op;
        if (parser->current_token->type == TOKEN_EQUAL) {
            parser_eat(parser, TOKEN_EQUAL);
            parser_eat(parser, TOKEN_TO);
            comparison_op = TOKEN_EQUAL;
        } else if (parser->current_token->type == TOKEN_LESS) {
            parser_eat(parser, TOKEN_LESS);
            parser_eat(parser, TOKEN_THAN);
            comparison_op = TOKEN_LESS;
        } else {
            fprintf(stderr, "Parser error: Expected 'equal' or 'less' after 'is' at line %d\n", parser->current_token->line);
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
        } else if (parser->current_token->type == TOKEN_RETURN) {
            stmt = parser_parse_return_statement(parser);
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

    if (parser->current_token->type == TOKEN_OTHERWISE) {
        parser_eat(parser, TOKEN_OTHERWISE);
        parser_eat(parser, TOKEN_COLON);
        else_body = parser_parse_statement_block(parser, &else_body_count);
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
        } else if (parser->current_token->type == TOKEN_IF) {
            stmt = parser_parse_if_statement(parser);
        } else if (parser->current_token->type == TOKEN_WHILE) {
            stmt = parser_parse_while_statement(parser);
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
        } else if (expr->type == EXPR_COMPARISON) {
            expression_destroy(expr->data.comparison.left);
            expression_destroy(expr->data.comparison.right);
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