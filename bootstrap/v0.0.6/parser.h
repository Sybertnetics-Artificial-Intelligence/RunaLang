#ifndef PARSER_H
#define PARSER_H

#include "lexer.h"

typedef enum {
    EXPR_INTEGER,
    EXPR_VARIABLE,
    EXPR_BINARY_OP,
    EXPR_COMPARISON,
    EXPR_FUNCTION_CALL,
    EXPR_STRING_LITERAL,
    EXPR_FIELD_ACCESS,
    EXPR_TYPE_NAME
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
        struct {
            char *function_name;
            struct Expression **arguments;
            int argument_count;
        } function_call;
        char *string_literal;
        struct {
            struct Expression *object;
            char *field_name;
        } field_access;
        char *type_name;  // For EXPR_TYPE_NAME
    } data;
} Expression;

typedef enum {
    STMT_LET,
    STMT_SET,
    STMT_RETURN,
    STMT_IF,
    STMT_WHILE,
    STMT_PRINT,
    STMT_EXPRESSION
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
            char *field_name;  // Optional field name for struct field assignment
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
        struct {
            Expression *expression;
        } print_stmt;
        struct {
            Expression *expression;
        } expr_stmt;
    } data;
} Statement;

typedef struct {
    char *name;
    char *type; // "Integer" for now
} Parameter;

typedef struct {
    char *name;
    char *type; // "Integer" or custom type name
    int offset; // Offset in struct memory layout
    int size;   // Size of this field in bytes
} TypeField;

typedef struct {
    char *name;
    TypeField *fields;
    int field_count;
    int size; // Total size of the struct
} TypeDefinition;

typedef struct {
    char *name;
    Parameter *parameters;
    int parameter_count;
    char *return_type;
    Statement **statements;
    int statement_count;
} Function;

typedef struct {
    Function **functions;
    int function_count;
    int function_capacity;
    TypeDefinition **types;
    int type_count;
    int type_capacity;
} Program;

typedef struct {
    Lexer *lexer;
    Token *current_token;
    Program *current_program;  // To access types during parsing
} Parser;

Parser* parser_create(Lexer *lexer);
void parser_destroy(Parser *parser);
Program* parser_parse_program(Parser *parser);
void program_destroy(Program *program);
void expression_destroy(Expression *expr);

#endif