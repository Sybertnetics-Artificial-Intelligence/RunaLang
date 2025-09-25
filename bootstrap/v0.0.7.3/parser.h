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
    EXPR_TYPE_NAME,
    EXPR_BUILTIN_CALL,
    EXPR_VARIANT_CONSTRUCTOR,
    EXPR_FUNCTION_POINTER,
    EXPR_ARRAY_INDEX
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
        struct {
            TokenType builtin_type;  // TOKEN_READ_FILE or TOKEN_WRITE_FILE
            struct Expression **arguments;
            int argument_count;
        } builtin_call;
        struct {
            char *type_name;      // Name of the ADT type (e.g., "Shape")
            char *variant_name;   // Name of the variant (e.g., "Circle")
            struct Expression **field_values; // Values for variant fields
            int field_count;
        } variant_constructor;
        struct {
            char *function_name;  // Name of the function being pointed to
            struct TypeDefinition *signature; // Function signature type information
        } function_pointer;
        struct {
            struct Expression *array;  // Array expression being indexed
            struct Expression *index;  // Index expression
        } array_index;
    } data;
} Expression;

typedef struct MatchCase {
    char *variant_name;        // e.g., "Circle"
    char **field_names;        // e.g., ["radius"]
    int field_count;
    struct Statement **body;   // Statements to execute for this case
    int body_count;
} MatchCase;

typedef enum {
    STMT_LET,
    STMT_SET,
    STMT_RETURN,
    STMT_IF,
    STMT_WHILE,
    STMT_PRINT,
    STMT_EXPRESSION,
    STMT_MATCH,
    STMT_IMPORT,
    STMT_BREAK,
    STMT_CONTINUE,
    STMT_INLINE_ASSEMBLY
} StatementType;

typedef struct Statement {
    StatementType type;
    union {
        struct {
            char *variable_name;
            Expression *expression;
        } let_stmt;
        struct {
            Expression *target;  // Target expression (variable or field access chain)
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
        struct {
            Expression *expression;  // Expression to match on
            struct MatchCase *cases;
            int case_count;
        } match_stmt;
        struct {
            char *filename;
            char *module_name;
        } import_stmt;
        struct {
            // Break statement has no additional data
        } break_stmt;
        struct {
            // Continue statement has no additional data
        } continue_stmt;
        struct {
            char **assembly_lines;           // Array of assembly instruction strings
            char **assembly_notes;           // Array of Note: comments
            int assembly_line_count;         // Number of assembly lines
            char **output_constraints;       // Output constraint strings
            int output_count;
            char **input_constraints;        // Input constraint strings
            int input_count;
            char **clobber_list;            // Clobber register list
            int clobber_count;
        } inline_assembly_stmt;
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

typedef enum {
    TYPE_KIND_STRUCT,   // Traditional struct/record type
    TYPE_KIND_VARIANT,  // ADT/variant/sum type
    TYPE_KIND_FUNCTION, // Function pointer type
    TYPE_KIND_ARRAY     // Fixed-size array type
} TypeKind;

typedef struct {
    char *name;          // Variant name (e.g., "Circle", "Rectangle")
    TypeField *fields;   // Fields for this variant
    int field_count;
    int tag;            // Unique tag for this variant (0, 1, 2, ...)
} Variant;

typedef struct {
    char *name;
    TypeKind kind;
    union {
        // For TYPE_KIND_STRUCT
        struct {
            TypeField *fields;
            int field_count;
        } struct_type;

        // For TYPE_KIND_VARIANT
        struct {
            Variant *variants;
            int variant_count;
        } variant_type;

        // For TYPE_KIND_FUNCTION
        struct {
            char **param_types;    // Array of parameter type names
            int param_count;       // Number of parameters
            char *return_type;     // Return type name
        } function_type;

        // For TYPE_KIND_ARRAY
        struct {
            char *element_type;    // Type of array elements
            int element_size;      // Size of each element in bytes
            int length;           // Number of elements in array
        } array_type;
    } data;
    int size; // Total size (including tag for variants)
} TypeDefinition;

typedef struct {
    char *name;
    Parameter *parameters;
    int parameter_count;
    char *return_type;
    Statement **statements;
    int statement_count;
} Function;

typedef struct Import {
    char *filename;
    char *module_name;
} Import;

typedef struct GlobalVariable {
    char *name;
    char *type;
    Expression *initial_value;  // Initial value expression (optional)
} GlobalVariable;

typedef struct {
    Function **functions;
    int function_count;
    int function_capacity;
    TypeDefinition **types;
    int type_count;
    int type_capacity;
    Import **imports;
    int import_count;
    int import_capacity;
    GlobalVariable **globals;
    int global_count;
    int global_capacity;
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