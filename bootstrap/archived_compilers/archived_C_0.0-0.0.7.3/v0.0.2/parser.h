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
#ifndef PARSER_H
#define PARSER_H

#include "lexer.h"

typedef enum {
    EXPR_INTEGER,
    EXPR_VARIABLE,
    EXPR_BINARY_OP,
    EXPR_COMPARISON
} ExpressionType;

typedef struct Expression {
    ExpressionType type;
    union {
        int integer_value;
        char *variable_name;
        struct {
            struct Expression *left;
            struct Expression *right;
            TokenType operator;
        } binary_op;
        struct {
            struct Expression *left;
            struct Expression *right;
            TokenType comparison_op; // TOKEN_EQUAL, TOKEN_LESS
        } comparison;
    } data;
} Expression;

typedef enum {
    STMT_LET,
    STMT_SET,
    STMT_RETURN,
    STMT_IF,
    STMT_WHILE
} StatementType;

typedef struct Statement {
    StatementType type;
    union {
        struct {
            char *variable_name;
            Expression *expression;
        } let_stmt;
        struct {
            char *variable_name;
            Expression *expression;
        } set_stmt;
        struct {
            Expression *expression;
        } return_stmt;
        struct {
            Expression *condition;
            struct Statement **if_body;
            int if_body_count;
            struct Statement **else_body;
            int else_body_count;
        } if_stmt;
        struct {
            Expression *condition;
            struct Statement **body;
            int body_count;
        } while_stmt;
    } data;
} Statement;

typedef struct {
    Statement **statements;
    int statement_count;
    int statement_capacity;
} Program;

typedef struct {
    Lexer *lexer;
    Token *current_token;
} Parser;

Parser* parser_create(Lexer *lexer);
void parser_destroy(Parser *parser);
Program* parser_parse_program(Parser *parser);
void program_destroy(Program *program);
void expression_destroy(Expression *expr);

#endif